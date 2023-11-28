/*DZ7*/

/*Baca nekih 8 errora, ali ispisuje ono sto treba :) */

/* Učitavanje dataseta SASHELP.IRIS */
data work.iris;
   set sashelp.iris;
run;

/* Zadrzati samo sepal length i width i samo za vrstu virginica */
data IRIS;
   set work.iris;
   keep SepalLength SepalWidth;
   where Species="Virginica";
run;

/*slijede: a) b) c) d)*/

/*** NEPARAMETARSKI BOOTSTRAP - macro JACKBOOT***/

/*** Primjer 1: Bootstrap   procjena korelacijskog koeficijenta ***/

      proc corr noprint data=iris
         out=out ;
         var SepalLength SepalWidth;
          
      run;

	  /*** filtriramo (zadrzimo samo jedan redak) i promijenimo ime (korelac.koef.) iz SepalWidth u bootcorr ***/
      proc corr noprint data=iris
         out=out(where=(_type_='CORR' & _name_='SepalLength')
                  rename=(SepalWidth=bootcorr)
                  keep=SepalWidth _TYPE_ _NAME_  );
         var SepalLength SepalWidth;
          
      run;

	  /*** ANALYZE macro je potrebno definirati prije poziva JACKBOOT macro-a ***/
	  /*** U ANALYZE macro treba 
	         dodati naredbu  %bystmt; 
	         dodati &by macro varijablu 
	         promijeniti ime ulaznog dataseta u macro varijablu &data
	         promijeniti ime izlaznog dataseta u macro varijablu &out  ****/

%macro analyze(data=,out=);
      proc corr noprint data=&data
         out=&out(where=(_type_='CORR' & _name_='SepalLength')
                  rename=(SepalWidth=bootcorr)
                  keep=SepalWidth _TYPE_ _NAME_ &by);
         var SepalLength SepalWidth;
         %bystmt;
      run;
%mend;

/** Izvo�enje JACKBOOT macro-a (dovoljno je samo prvi puta) ***/

 %let nboot=1000;
 %let seed=3774;

%include "/home/u63365319/ZRINKA/jackboot.sas";  
   %boot(data=iris, random=&seed, samples=&nboot)

   /** Bootstrap vrijednosti se (nakon izvodenja BOOT macro-a) nalaze u datasetu work.BOOTDIST (varijabla BOOTCORR)***/
 /** 90% Interval pouzdanosti percentilnom metodom: p5-p95 ***/
   proc means data=bootdist mean std p5 p95;
    var bootcorr;
   run;

   
 /*** Primjer 2: Bootstrap procjena regresijskog koeficijenta ***/

   proc reg data=iris noprint outest=out;                                                                                     
                                                                                                                                             
    model SepalWidth=SepalLength; 
	run; quit;
 
 /*** filtriramo (zadrzimo samo jedan redak) i promijenimo ime (regresijskog koef.) iz SepalLength u bootreg ***/

	proc reg data=iris noprint outest=out(where=(_type_='PARMS')                                                                                
                  rename=(SepalLength=bootreg)                                                                                                          
                  keep=SepalLength _type_);                                                                                     
    model SepalWidth=SepalLength; 
    run; quit;

	  /*** ANALYZE macro je potrebno definirati prije poziva JACKBOOT macro-a ***/
	  /*** U ANALYZE macro treba 
	         dodati naredbu  %bystmt; 
	         dodati &by macro varijablu 
	         promijeniti ime ulaznog dataseta u macro varijablu &data
	         promijeniti ime izlaznog dataseta u macro varijablu &out  ****/

%macro analyze(data=,out=);
		proc reg data=&data noprint outest=&out(where=(_type_='PARMS')                                                                                
                  rename=(SepalLength=bootreg)                                                                                                          
                  keep=SepalLength _type_  &by);                                                                                     
    model SepalWidth=SepalLength; 
	 %bystmt;
    run; quit;
%mend;

   %boot(data=iris, random=&seed, samples=&nboot)

   /** Bootstrap vrijednosti se (nakon izvodenja BOOT macro-a) nalaze u datasetu work.BOOTDIST (varijabla BOOTCORR)***/
 /** 90% Interval pouzdanosti percentilnom metodom: p5-p95 ***/
   proc means data=bootdist mean std p5 p95;
    var bootreg;
   run;




   /** Dodatno mozemo izvesti %ALLCI macro, za procjenu svih bootstrap intervala pouzdanosti **/
   /** %boot i %allci su definirani u %jackboot macro-u **/
   /** U pozivu %allci mozemo definirati alpha vrijednost za interval pouzdanosti **/

   %allci(alpha=0.10,stat=bootreg) 

  /*** AKO zadrzimo vise varijabli (sa keep= opcijom), (napr. intercept, _RMSE_ (drugi korjen iz procjene varijance pogre�ke) 
       onda ce se bootstrap izvesti za sve zadrzane varijable ***/


%macro analyze(data=,out=);
		proc reg data=&data noprint outest=&out(where=(_type_='PARMS')                                                                                
                  rename=(SepalLength=bootreg)                                                                                                          
                  keep=SepalLength _type_ _RMSE_ intercept &by);                                                                                     
    model SepalWidth=SepalLength; 
	 %bystmt;
    run; quit;
%mend;


   %boot(data=iris,random=&seed, samples=&nboot)

   proc means data=bootdist mean std p5 p95;
    var bootreg _RMSE_ intercept;
   run;

      %allci(alpha=0.10,stat=bootreg _RMSE_ intercept)


/*** Primjer 3: MEANS ***/

	  proc means data=iris noprint  nway;                                                                                
   var SepalWidth;                                                                                                                           
   output out=out(drop=_freq_ _type_) mean=mean stderr=stde; 
         
 run; 
 
/** Izvodenje JACKBOOT macro-a (dovoljno je samo prvi puta) ***/

 %let nboot=1000;
 %let seed=3774;

%include "/home/u63365319/ZRINKA/jackboot.sas";  
   %boot(data=iris,random=&seed, samples=&nboot)

   /** Bootstrap vrijednosti se (nakon izvodenja BOOT macro-a) nalaze u datasetu work.BOOTDIST (varijabla BOOTCORR)***/

 /** 95% Interval pouzdanosti percentilnom metodom: p2.5-p97.5***/
   proc means data=bootdist mean std alpha=0.05;
   	var bootcorr;
   run;

   
 /*** Primjer 2: Bootstrap procjena regresijskog koeficijenta ***/

   proc reg data=iris noprint outest=out;                                                                                     
                                                                                                                                             
    model SepalWidth=SepalLength; 
	run; quit;
 
 /*** filtriramo (zadrzimo samo jedan redak) i promijenimo ime (regresijskog koef.) iz SepalLength u bootreg ***/

	proc reg data=iris noprint outest=out(where=(_type_='PARMS')                                                                                
                  rename=(SepalLength=bootreg)                                                                                                          
                  keep=SepalLength _type_);                                                                                     
    model SepalWidth=SepalLength; 
    run; quit;

	  /*** ANALYZE macro je potrebno definirati prije poziva JACKBOOT macro-a ***/
	  /*** U ANALYZE macro treba 
	         dodati naredbu  %bystmt; 
	         dodati &by macro varijablu 
	         promijeniti ime ulaznog dataseta u macro varijablu &data
	         promijeniti ime izlaznog dataseta u macro varijablu &out  ****/

%macro analyze(data=,out=);
		proc reg data=&data noprint outest=&out(where=(_type_='PARMS')                                                                                
                  rename=(SepalLength=bootreg)                                                                                                          
                  keep=SepalLength _type_  &by);                                                                                     
    model SepalWidth=SepalLength; 
	 %bystmt;
    run; quit;
%mend;

   %boot(data=iris,random=&seed, samples=&nboot)

   /** Bootstrap vrijednosti se (nakon izvodnja BOOT macro-a) nalaze u datasetu work.BOOTDIST (varijabla BOOTCORR)***/
 /** 90% Interval pouzdanosti percentilnom metodom: p5-p95 ***/
   proc means data=bootdist mean std alpha=0.05;
   	var bootreg;
   run;




   /** Dodatno mozemo izvesti %ALLCI macro, za procjenu svih bootstrap intervala pouzdanosti **/
   /** %boot i %allci su definirani u %jackboot macro-u **/
   /** U pozivu %allci mozemo definirati alpha vrijednost za interval pouzdanosti **/

   %allci(alpha=0.05,stat=bootreg) 

  /*** AKO zadrzimo vise varijabli (sa keep= opcijom), (napr. intercept, _RMSE_ (drugi korjen iz procjene varijance pogre�ke) 
       onda ce se bootstrap izvesti za sve zadrzane varijable ***/


%macro analyze(data=,out=);
		proc reg data=&data noprint outest=&out(where=(_type_='PARMS')                                                                                
                  rename=(SepalLength=bootreg)                                                                                                          
                  keep=SepalLength _type_ _RMSE_ intercept &by);                                                                                     
    model SepalWidth=SepalLength; 
	 %bystmt;
    run; quit;
%mend;3


   %boot(data=iris,random=&seed, samples=&nboot)

   proc means data=bootdist mean std alpha=0.05;
    var bootreg _RMSE_ intercept;
   run;

      %allci(alpha=0.05,stat=bootreg _RMSE_ intercept)


/*** Primjer 3: MEANS ***/

	  proc means data=iris noprint  nway;                                                                                
   var SepalWidth;                                                                                                                           
   output out=out(drop=_freq_ _type_) mean=mean stderr=stde; 
         
 run;


 
/** Primjer preuzet iz "268-2010 SUGI Bootstrap.pdf", str.3 (u folderu "Downloaded Papers 2012") **/

proc surveyselect data=IRIS out=outboot
seed=4455
method=urs
samprate=1
outhits
rep=100; /*1000*/
run;


ods listing close;

proc corr data=outboot
out=outall(where=(_type_='CORR' & _name_='SepalLength')
                  rename=(SepalWidth=corr)
                  keep=SepalWidth _TYPE_ _NAME_  );
         var SepalLength SepalWidth;
by replicate;
run;

ods listing;

/** bootsrtap percentilni 95%CI za korelacijski koeficijent ***/
proc univariate data=outall;
var corr;
output out=final95 pctlpts=2.5, 97.5 pctlpre=ci_ ;
run;
 
proc print data=final95;
run;

/** bootsrtap percentilni 90%CI za korelacijski koeficijent ***/

proc univariate data=outall;
var corr;
output out=final90 pctlpts=5, 95 pctlpre=ci_ ;
run;
 
proc print data=final90;
run;

/*e)*/
proc univariate data=bootdist noprint;
var bootreg;
histogram bootreg / normal;
run;