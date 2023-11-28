/*DZ2 ZRINKA PECANIC 0036517187*/
/*ZAD1*/

/*ZAD1*/
%macro mrantbl(dat,catvar,pvar,rep,seed);

proc freq data=zrinka.dob_hrvata_popis2001;
   where spol="Z" and starost ge 18 and starost le 30;
    table starost /noprint out=zrinka.dob_zenaHR_18_30(keep=starost percent count);
    weight frek;
run;
data zrinka.dob_zenaHR_18_30;
   set zrinka.dob_zenaHR_18_30;
   dprob=percent/100;
run;

%mend mrantbl;

/* %mrantbl(dat=zrinka.dob_zenaHR_18_30,catvar=starost,pvar=DPROB,rep=1000,seed=123) */
%mrantbl(dat=zrinka.dob_zenaHR_18_30,catvar=starost,pvar=DPROB,rep=10000,seed=123) 

/*ZAD2*/

data _null_;
    call streaminit(87736);
run;
/* Generate customer data */
data customers;
    do i = 1 to 100;
        /* Generate random number for customer type */
        customer_type = rand("Bernoulli", 0.25);
        if customer_type = 1 then do;
            /* Exponential distribution for purchase time */
            purchase_time = rand("Exponential", 2.5);
        end;
        else do;
            /* Erlang distribution for purchase time, shape = 2, scale = 4/shape = 2 */
            purchase_time = rand("Gamma", 2, 2);
        end;
        output;
    end;
    keep purchase_time;
run;

/* Calculate moments and total shopping time */
proc means data=customers mean std skewness kurtosis sum;
   title "ZAD2 customer data";
run;
/*a*/


/*ZAD3*/
data RAZRED; 
   input Name $ Height Weight @@; 
   datalines; 
Alfred  81.0 130.5   Alice  56.5  84.0   Barbara 65.3  98.0 
Carol   62.8 102.5   Henry  61.5 101.5   James   76.3 170.0 
Jane    71.8  94.5   Janet  62.5 112.5   Jeffrey 61.5  85.0 
John    59.0  99.5   Joyce  65.3 150.5   Judy    64.3  90.0 
Louise  56.3  77.0   Mary   66.5 115.0   Philip  72.5 152.0 
Robert  64.8 158.0   Ronald 67.0 137.0   Thomas  57.5  85.0 	
; 
run;

/*a*/

data RAZRED;
  set RAZRED;
  Visina = Height * 2.54; /* convert inches to centimeters */
  drop Height; /* drop the old height column */
  Tezina = Weight * 0.45359237; /* convert pounds to kilograms */
  drop Weight; /* drop the old weight column */
run;

/*b*/
proc means data=RAZRED mean std skewness kurtosis;
   var Visina Tezina;
   title "ZAD3 b)";
run;

/*c*/



/* Generate 18 random numbers using the values of the first 4 moments estimated for Visina */
data random_c;
   call streaminit(63478);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation*/
      x=rand('NORMAL', 165.4386667, 17.0788823);
      output;
   end;
run;

/* Estimate the first 4 moments of the generated 18 numbers */
proc means data=random_c mean std skewness kurtosis;
   var x;
   title "ZAD3 c)";
run;

/*d*/
/* Set the seed */


/* Generate 18 random numbers */
data random_d;
   call streaminit(2211);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation */
      x=rand('NORMAL', 51.4701342, 13.1600365);
      output;
   end;
run;

/* Estimate the first 4 moments of the generated 18 numbers */
proc means data=random_d mean std skewness kurtosis;
   var x;
   title "ZAD3 d)";
run;

/*e*/
/*seeds: 33456, 4544, 4236, 56643*/



/* Generate 18 random numbers using the values of the first 4 moments estimated for Visina */
data random_e1;
   call streaminit(33456);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation*/
      x=rand('NORMAL', 165.4386667, 17.0788823);
      output;
   end;
run;

/* Estimate the first 4 moments of the generated 18 numbers */
proc means data=random_e1 mean std skewness kurtosis;
   var x;
   title "seed 33456 visina";
run;

data random_e2;
   call streaminit(33456);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation */
      x=rand('NORMAL', 51.4701342, 13.1600365);
      output;
   end;
run;

/* Estimate the first 4 moments of the generated 18 numbers */
proc means data=random_e2 mean std skewness kurtosis;
   var x;
   title "seed 33456 tezina";
run;



/* Generate 18 random numbers using the values of the first 4 moments estimated for Visina */
data random_e3;
   call streaminit(4544);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation*/
      x=rand('NORMAL', 165.4386667, 17.0788823);
      output;
   end;
run;

/* Estimate the first 4 moments of the generated 18 numbers */
proc means data=random_e3 mean std skewness kurtosis;
   var x;
   title "seed 4544 visina";
run;

data random_e4;
   call streaminit(4544);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation */
      x=rand('NORMAL', 51.4701342, 13.1600365);
      output;
   end;
run;

/* Estimate the first 4 moments of the generated 18 numbers */
proc means data=random_e4 mean std skewness kurtosis;
   var x;
   title "seed 4544 tezina";
run;



/* Generate 18 random numbers using the values of the first 4 moments estimated for Visina */
data random_e5;
   call streaminit(4236);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation*/
      x=rand('NORMAL', 165.4386667, 17.0788823);
      output;
   end;
run;

/* Estimate the first 4 moments of the generated 18 numbers */
proc means data=random_e5 mean std skewness kurtosis;
   var x;
   title "seed 4236 visina";
run;

data random_e6;
   call streaminit(4236);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation */
      x=rand('NORMAL', 51.4701342, 13.1600365);
      output;
   end;
run;

/* Estimate the first 4 moments of the generated 18 numbers */
proc means data=random_e6 mean std skewness kurtosis;
   var x;
   title "seed 4236 tezina";
run;



/* Generate 18 random numbers using the values of the first 4 moments estimated for Visina */
data random_e7;
   call streaminit(56643);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation*/
      x=rand('NORMAL', 165.4386667, 17.0788823);
      output;
   end;
run;


proc means data=random_e7 mean std skewness kurtosis;
   var x;
   title "seed 56643 visina";
run;

data random_e8;
   call streaminit(56643);
   do i=1 to 18;
      /* generate random numbers using the estimated mean, standard deviation */
      x=rand('NORMAL', 51.4701342, 13.1600365);
      output;
   end;
run;


proc means data=random_e8 mean std skewness kurtosis;
   var x;
   title "seed 56643 tezina";
run;

/*ZAD4*/
/*a*/

data _null_;
 call streaminit(47755);
run;

* Generiranje vremena potrebnog za kupovinu u trgovini A;
data trgovinaA;
 do i = 1 to 300;
  kupac = i;
  rnd = rand("uniform");
  if rnd < 0.3 then do;
   vrijeme = rand("exponential", 3);
  end;
  else do;
   vrijeme = rand("gamma", 5, 1);
  end;
  output;
 end;
run;

* Generiranje vremena potrebnog za kupovinu u trgovini B;
data trgovinaB;
 do i = 1 to 300;
  kupac = i;
  rnd = rand("uniform");
  if rnd < 0.4 then do;
   vrijeme = rand("exponential", 4);
  end;
  else do;
   vrijeme = rand("gamma", 7, 1);
  end;
  output;
 end;
run;
/*b i c*/
proc means data=trgovinaA mean std skewness kurtosis sum;
   var vrijeme;
   title "Trgovina A original";
run; /* suma=ukupno vrijeme za uslužiti sve kupce = 1372 min tj. cca 23h*/
/* prosjek = 4.57 min po kupcu, znači da u jednom radnom danu od 12h može bit uslužen 157 kupac*/

proc means data=trgovinaB mean std skewness kurtosis sum;
   var vrijeme;
   title "Trgovina B original";
run; /* suma=ukupno vrijeme za uslužiti sve kupce = 1688 min tj. cca 28h*/
/* prosjek = 5.63 min po kupcu, znači da u jednom  danu može bit usluženo 128 kupaca*/

/*d*/
data trgovinaA2;
 do i = 1 to 300;
  kupac = i;
  rnd = rand("uniform");
  if rnd < 0.3 then do;
   vrijeme = rand("exponential", 3);
  end;
  else do;
   vrijeme = rand("exponential", 5);
  end;
  output;
 end;
run;

* Generiranje vremena potrebnog za kupovinu u trgovini B;
data trgovinaB2;
 do i = 1 to 300;
  kupac = i;
  rnd = rand("uniform");
  if rnd < 0.4 then do;
   vrijeme = rand("exponential", 4);
  end;
  else do;
   vrijeme = rand("exponential", 7);
  end;
  output;
 end;
run;

/*e i f*/
proc means data=trgovinaA2 mean std skewness kurtosis sum;
   var vrijeme;
   title "Trgovina A edited";
run; /* suma=ukupno vrijeme za uslužiti sve kupce = 1323 min tj. cca 22h*/
/* prosjek = 4.41 min po kupcu, znači da u jednom radnom danu od 12h može biti usluženo 163 kupaca*/

proc means data=trgovinaB2 mean std skewness kurtosis sum;
   var vrijeme;
   title "Trgovina B edited";
run; /* suma=ukupno vrijeme za uslužiti sve kupce = 1819 min tj. cca 30h*/
/* prosjek = 6.07 min po kupcu, znači da u jednom radnom danu od 12h može biti usluženo 118 kupaca*/

/*g*/
data trgovinaAg;
 do i = 1 to 10000;
  kupac = i;
  rnd = rand("uniform");
  if rnd < 0.3 then do;
   vrijeme = rand("exponential", 3);
  end;
  else do;
   vrijeme = rand("gamma", 5, 1);
  end;
  output;
 end;
run;

* Generiranje vremena potrebnog za kupovinu u trgovini B;
data trgovinaBg;
 do i = 1 to 10000;
  kupac = i;
  rnd = rand("uniform");
  if rnd < 0.4 then do;
   vrijeme = rand("exponential", 4);
  end;
  else do;
   vrijeme = rand("gamma", 7, 1);
  end;
  output;
 end;
run;

proc means data=trgovinaAg mean std skewness kurtosis stderr sum;
   var vrijeme;
   title "g) Trgovina A";
run;

proc means data=trgovinaBg mean std skewness kurtosis stderr sum;
   var vrijeme;
   title "g) Trgovina B";
run;

/*h*/
data trgovinaA2h;
 do i = 1 to 10000;
  kupac = i;
  rnd = rand("uniform");
  if rnd < 0.3 then do;
   vrijeme = rand("exponential", 3);
  end;
  else do;
   vrijeme = rand("exponential", 5);
  end;
  output;
 end;
run;

* Generiranje vremena potrebnog za kupovinu u trgovini B;
data trgovinaB2h;
 do i = 1 to 10000;
  kupac = i;
  rnd = rand("uniform");
  if rnd < 0.4 then do;
   vrijeme = rand("exponential", 4);
  end;
  else do;
   vrijeme = rand("exponential", 7);
  end;
  output;
 end;
run;

proc means data=trgovinaA2h mean std skewness kurtosis stderr sum;
   var vrijeme;
   title "h) Trgovina A";
run;

proc means data=trgovinaB2h mean std skewness kurtosis stderr sum;
   var vrijeme;
   title "h) Trgovina B";
run;



/*ZAD5*/

data TLAK;
	input SKTprije SKTposlije @@;
    datalines;
120 127   128 130   130 131   118 127
140 132   128 125   140 141   135 137
126 118   130 132   130 129   127 120
122 121   141 125  
;
run;


/*a*/
ods output ttests=ttests;
   proc ttest data=tlak;
   paired SKTprije* SKTposlije;
   title "Upareni t test";
   RUN; /*p > 0.05, ne možemo odbaciti H0*/


/*b*/

data TLAK_gen;
  /* Set seed for replicability */
  call streaminit(56178);

  /* Get mean, std, and corr from original data */
  proc means data=TLAK mean std;
    var SKTprije SKTposlije;
  run;
  proc corr data=TLAK;
    var SKTprije SKTposlije;
  run;

  /* Define parameters for normal distribution */
  *%let mean1 = 129.6428571;
  *%let std1 = 7.2600820;
  *%let mean2 = 128.2142857;
  *%let std2 = 6.3751751;
  *%let corr = 0.54358;
/*Odavde baca neke errore*/
  /* Generate 100 values for SKTprije and SKTposlije */
  *do rep = 1 to 100;
    /* Generate two normally distributed values */
   * x = rannor(56178);
    *y = rannor(56178);

    /* Transform to bivariate normal distribution */
    *z1 = &mean1 + &std1 * x;
    *z2 = &mean2 + &corr * &std2 * x + &std2 * sqrt(1 - &corr**2) * y;

    /* Add to output data */
    *output;
  *end;
*run;

/* Compare means and std */
/*proc means data=TLAK_gen TLAK;
  var SKTprije SKTposlije;
  output out=means;
run;*/

/* Compare correlation coefficients */
/*proc corr data=TLAK_gen TLAK;
  var SKTprije SKTposlije;
run;*/