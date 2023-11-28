/*ZAD1*/


/** CHAPTER1_2_T_GAMMA3.sas **/

/** t values from GAMMA random samples of different sizes **/

%LET SEED =123578;		%LET K=0.5; /*shape parameter of the gamma distribution */
%LET NREPtot=100000;	%LET beta=1; /*scale parameter of the gama distribution */
%let nn=10 20 30 50 100 200;
%let nrep=10000;

%let mu=%sysevalf(&k/&beta); /* expected value of Gamma(&k, &beta) */

proc datasets library=work;
 delete tall;
run; quit;

%macro nsize;

%let kk=1; 
%let n=%scan(&nn,&kk); 
%do %while(&n NE); 

DATA RAW;
 N=&N;
 CALL STREAMINIT(&SEED);
 DO REP = 1 TO &NREP;
 DO I=1 to &N;
  X = RAND ("GAMMA",&k);
  XT = X - &mu;
  OUTPUT;
 END;
 END;
 label rep='repetition';
RUN;
                                                                                      
proc means data=raw noprint;                                                                                              
  var xt;                                                                                                         
  by rep;                                                                                                        
  output out=t mean=mean stderr=stderr t=t; 
  id n;
run; 

proc append base=tall data=t;
run;
   %let kk=%eval(&kk+1); 
   %let n=%scan(&nn,&kk); 
%end; 
%mend nsize;

%nsize;


  /* Boxplot */
title1 "t values from Gamma, n=&nn";

proc sgplot data=tall;
 vbox t/group=n;
 refline 0;
 run;


proc means data=tall mean std stderr skewness kurtosis maxdec=3;
   var t;
   class n;
run;

/* Distribution analysis of means by sample sizes N */
proc sgplot data = tall;
  title "Distribution of Means by Sample Sizes N";
  histogram mean / group = n;
  density mean / group = n;
  xaxis label = "Mean";
  yaxis label = "Density";
run;

/* Distribution analysis of t-statistics by sample sizes N */
proc sgplot data = tall;
  title "Distribution of t-Statistics by Sample Sizes N";
  histogram t / group = n;
  density t / group = n;
  xaxis label = "t-Statistic";
  yaxis label = "Density";
run;

proc means data = tall mean std stderr skewness kurtosis maxdec = 3;
  var t;
  class n;
run;

title;


/** CHAPTER1_2_T_GAMMA3.sas **/

/** t values from UNIFORM random samples of different sizes **/

%LET SEED = 123578;
%LET NREPtot = 100000;
%LET nn = 10 20 30 50 100 200;
%LET nrep = 10000;

data _null_;
  call streaminit(&SEED);
  mu = mean(rand("UNIFORM", 0, 1));
  call symputx('MU', mu);
run;

proc datasets library=work;
  delete tall;
run;
quit;

%macro nsize;
  %let kk = 1;
  %let n = %scan(&nn, &kk);
  %do %while(&n NE);
    DATA RAW;
      N = &N;
      CALL STREAMINIT(&SEED);
      DO REP = 1 TO &NREP;
        DO I = 1 to &N;
          X = RAND("UNIFORM");
          XT = X - &mu;
          OUTPUT;
        END;
      END;
      label rep = 'repetition';
    RUN;

    proc means data = raw noprint;
      var xt;
      by rep;
      output out = t mean = mean stderr = stderr t = t;
      id n;
    run;

    proc append base = tall data = t;
    run;

    %let kk = %eval(&kk + 1);
    %let n = %scan(&nn, &kk);
  %end;
%mend nsize;

%nsize;

/* Boxplot */
title1 "t values from Uniform, n = &nn";

proc sgplot data = tall;
  vbox t / group = n;
  refline 0;
run;

/* Distribution analysis of means by sample sizes N */
proc sgplot data = tall;
  title "Distribution of Means by Sample Sizes N";
  histogram mean / group = n;
  density mean / group = n;
  xaxis label = "Mean";
  yaxis label = "Density";
run;

/* Distribution analysis of t-statistics by sample sizes N */
proc sgplot data = tall;
  title "Distribution of t-Statistics by Sample Sizes N";
  histogram t / group = n;
  density t / group = n;
  xaxis label = "t-Statistic";
  yaxis label = "Density";
run;

proc means data = tall mean std stderr skewness kurtosis maxdec = 3;
  var t;
  class n;
run;

title;

/*ZAD2*/


*******  Program for ANOVA Example: Assessing the Effect of Data Non-Normality on the Type I Error Rate in ANOVA  *************;
 
******* Note: RUN autoexec.sas program  ******************
*******       RUN fleishman macro       ******************;

%macro fleishman;
   /*	This program calculates the coefficients for Fleishman's power transformation in order     */
   /*   to obtain univariate non-normal variables.  For references, see Allen I. Fleishman, (1978).*/
   /*   A method for simulating non-normal distributions, Psychometrika, 43, 521-532.  Also see    */
   /*   Vale, C. David and Maurelli, Vincent A.  (1983).  Simulating multivariate non-normal       */
   /*   distributions, Psychometrika, 48, 465-471.                                                 */                   

PROC IML;

 use skewkurt; 
 read all var{skewness kurtosis} into skewkurt; 

START NEWTON;
  RUN FUN;
  DO ITER = 1 TO MAXITER
  WHILE(MAX(ABS(F))>CONVERGE);
        RUN DERIV;
        DELTA=-SOLVE(J,F);
        COEF=COEF+DELTA;
        RUN FUN;
  END;
FINISH NEWTON;
MAXITER=25;
CONVERGE=.000001;
START FUN;
  X1=COEF[1];
  X2=COEF[2];
  X3=COEF[3];
  F=(X1**2+6*X1*X3+2*X2**2+15*X3**2-1)//
    (2*X2*(X1**2+24*X1*X3+105*X3**2+2)-SKEWNESS)//
    (24*(X1*X3+X2**2*(1+X1**2+28*X1*X3)+X3**2*
      (12+48*X1*X3+141*X2**2+225*X3**2))-KURTOSIS);
FINISH FUN;
START DERIV;
  J=((2*X1+6*X3)||(4*X2)||(6*X1+30*X3))//
    ((4*X2*(X1+12*X3))||(2*(X1**2+24*X1*X3+105*X3**2+2))
     ||(4*X2*(12*X1+105*X3)))//
    ((24*(X3+X2**2*(2*X1+28*X3)+48*X3**3))||
     (48*X2*(1+X1**2+28*X1*X3+141*X3**2))||
     (24*(X1+28*X1*X2**2+2*X3*(12+48*X1*X3+141*X2**2+225*X3**2)
 
     +X3**2*(48*X1+450*X3))));
FINISH DERIV;
DO;
NUM = NROW(SKEWKURT);
DO VAR=1 TO NUM;
  SKEWNESS=SKEWKURT[VAR,1];
  KURTOSIS=SKEWKURT[VAR,2];
  COEF={1.0, 0.0, 0.0};
  RUN NEWTON;
  COEF=COEF`;
  SK_KUR=SKEWKURT[VAR,];
  COMBINE=SK_KUR || COEF;
  IF VAR=1 THEN RESULT=COMBINE;
  ELSE IF VAR>1 THEN RESULT=RESULT // COMBINE;
END;
  PRINT "COEFFICEINTS OF B, C, D FOR FLEISHMAN'S POWER TRANSFORMATION";
  PRINT "Y = A + BX + CX^2 + DX^3";
  PRINT " A = -C";
  MATTRIB RESULT COLNAME=({SKEWNESS KURTOSIS B C D})
                 FORMAT=12.9;
  PRINT RESULT;
END;
 create fleishman from result[colname={SKEWNESS KURTOSIS B C D}];
   append from result;

QUIT;
 
%mend fleishman;

***************************************************************************;


/*	In the following matrix 'SKEWKURT', specify the skewness and kurtosis for each variable.  */
/*  Each row represents one variable. In each row, the 1st number is the skewness, the 2nd is */
/*  the kurtosis of the variable;                                                             */

/* desired skewness, kurtosis */

data skewkurt;
 input skewness kurtosis;
 datalines;
 2.5  6
;
run;

%fleishman; 

                   * Fleishman coefficients for data shapes
                     1st row: non-normal data (aa=2), 2nd row: normal data (aa=1);
 

data fleishman;
 set fleishman;
 aa=2; output;
 aa=1; b=1; c=0; d=0; SKEWNESS=0; KURTOSIS=0; output;
run;



%MACRO ANOVA;

%DO A=1 %TO 2;        * A=1: normal data,  A=2: non-normal data;
%DO B=1 %TO 2;        * B=1: equal variance,  B=2: unequal variance;


%LET ALPHA=0.05;   * nominal Type I error rate;
 



                   * means and variances of 3 groups
	                 A=1: normal data, A=2:non-normal data
                     B=1: equal variances, B=2: unequal;
 
  * generate data for group 1;

data group1;
 merge fleishman(where=(aa=&a)) meanvar(where=(a=&a and b=&b and group=1));

 a=-c;
 DO REP=1 TO 1000;   * 1,000 replications in each cell;

 do i=1 to n;
    x=RANNOR(0);
	x=a + b*x + c* x**2 + d*x**3;
	x=mean + sqrt(var)* x;
	output;
 end;
 end;
run;

 * generate data for group 2;

data group2;
 merge fleishman(where=(aa=&a)) meanvar(where=(a=&a and b=&b and group=2));

 a=-c;
 DO REP=1 TO 1000;   * 1,000 replications in each cell;

 do i=1 to n;
    x=RANNOR(0);
	x=a + b*x + c* x**2 + d*x**3;
	x=mean + sqrt(var)* x;
	output;
 end;
 end;
run;

 * generate data for group 3;

data group3;
 merge fleishman(where=(aa=&a)) meanvar(where=(a=&a and b=&b and group=3));

 a=-c;
 DO REP=1 TO 1000;   * 1,000 replications in each cell;

 do i=1 to n;
    x=RANNOR(0);
	x=a + b*x + c* x**2 + d*x**3;
	x=mean + sqrt(var)* x;
	output;
 end;
 end;
run;

 
                  * combine 3 groups data, vertical concatenation;

data dataall;
 set group1 group2 group3;
 run;

proc sort data=dataall;
 by rep group;
 run;
 
 

                   * run ANOVA analysis, and output ANOVA results
                     to a SAS working data 'ANOVAOUT';

PROC ANOVA DATA=DATAALL NOPRINT OUTSTAT=ANOVAOUT;
  CLASS GROUP;
  MODEL X=GROUP;
  by rep;
RUN;
                    * use 'ANOVAOUT' data;
                    * extract relevant ANOVA results;

DATA AA; SET ANOVAOUT;
  IF _TYPE_='ANOVA';
  DF_MOD=DF; SS_MOD=SS;

                    * add a variable indicating statistical significance;
  IF PROB<&ALPHA THEN SIG='YES';
     ELSE SIG=' NO';

  KEEP DF_MOD SS_MOD F PROB SIG REP;     * keep relevant variables;

                    * extract error df, error sum-of-squares;

DATA BB; SET ANOVAOUT;
  IF _TYPE_='ERROR';
  DF_ERR=DF; SS_ERR=SS;
  KEEP DF_ERR SS_ERR REP;

                   * merge two data sets, add study design information;
DATA AB; MERGE AA BB;
by rep;
  IF &A=1 THEN NORMAL='YES';
     ELSE IF &A=2 THEN NORMAL=' NO';
  IF &B=1 THEN EQ_VAR='YES';
     ELSE IF &B=2 THEN EQ_VAR=' NO';
                    * append each replication results to a permanent SAS data;
PROC APPEND BASE=&resultsdataset;
RUN;

proc datasets library=work;
 delete dataall group1 group2 group3 aa bb ab;
 run; quit;

%END;         * close B do loop;
%END;         * close A do loop;

%MEND ANOVA;  * macro 'ANOVA';




/* desired mean, var, n for each group (=1,2,3) and each A and B */
/* A=1: normal data,  A=2: non-normal data                       */
/* B=1: equal variance,  B=2: unequal variance                   */

/*** FIRST RUN: Equal sample size per group and same variance ***/

%let resultsdataset=sasuser.ANOVA_same_n_30;  *Name of the dataset with the results of the MC experiment;
data meanvar;
 input A B group mean var n;
 datalines;
 1 1 1 50 20 30
 1 1 2 50 20 30
 1 1 3 50 20 30
 1 2 1 50 20 30
 1 2 2 50 20 30
 1 2 3 50 20 30
 2 1 1 50 20 30
 2 1 2 50 20 30
 2 1 3 50 20 30
 2 2 1 50 20 30
 2 2 2 50 20 30
 2 2 3 50 20 30
;
run;

*%ANOVA;       *run macro 'ANOVA';


    * obtain descriptive statistics for the simulation results;
DATA A; SET &resultsdataset;
PROC SORT; BY NORMAL EQ_VAR;
PROC FREQ; BY NORMAL EQ_VAR;
  TABLES SIG;
RUN;


/*** SECOND RUN: Equal sample size per group and unequal variances ***/

%let resultsdataset=sasuser.ANOVA_same_n_30;  *Name of the dataset with the results of the MC experiment;
data meanvar;
 input A B group mean var n;
 datalines;
 1 1 1 50 10 30
 1 1 2 50 20 30
 1 1 3 50 30 30
 1 2 1 50 10 30
 1 2 2 50 20 30
 1 2 3 50 30 30
 2 1 1 50 10 30
 2 1 2 50 20 30
 2 1 3 50 30 30
 2 2 1 50 10 30
 2 2 2 50 20 30
 2 2 3 50 30 30
;
run;

*%ANOVA;       *run macro 'ANOVA';


    * obtain descriptive statistics for the simulation results;
DATA A; SET &resultsdataset;
PROC SORT; BY NORMAL EQ_VAR;
PROC FREQ; BY NORMAL EQ_VAR;
  TABLES SIG;
RUN;
******************************************************************************************;


/*** THIRD RUN: Unequal sample size per group and same variance ***/


%let resultsdataset=sasuser.ANOVA_inpropvar_different_n_30;  *Name of the dataset with the results of the MC experiment;

data meanvar;
 input A B group mean var n;
 datalines;
 1 1 1 50 20 10
 1 1 2 50 20 30
 1 1 3 50 20 50
 1 2 1 50 20 10
 1 2 2 50 20 30
 1 2 3 50 20 50
 2 1 1 50 20 10
 2 1 2 50 20 30
 2 1 3 50 20 50
 2 2 1 50 20 10
 2 2 2 50 20 30
 2 2 3 50 20 50
;
run;

*%ANOVA;       * run macro 'ANOVA';

              * obtain descriptive statistics for the simulation results;
DATA A; SET &resultsdataset;
PROC SORT; BY NORMAL EQ_VAR;
PROC FREQ; BY NORMAL EQ_VAR;
  TABLES SIG;
RUN;
******************************************************************;

/*** FOURTH RUN: Unequal sample size per group and unequal variance ***/


%let resultsdataset=sasuser.ANOVA_inpropvar_different_n_30;  *Name of the dataset with the results of the MC experiment;

data meanvar;
 input A B group mean var n;
 datalines;
 1 1 1 50 20 10
 1 1 2 50 20 30
 1 1 3 50 20 50
 1 2 1 50 20 10
 1 2 2 50 20 30
 1 2 3 50 20 50
 2 1 1 50 20 10
 2 1 2 50 20 30
 2 1 3 50 20 50
 2 2 1 50 20 10
 2 2 2 50 20 30
 2 2 3 50 20 50
;
run;

*%ANOVA;       * run macro 'ANOVA';

              * obtain descriptive statistics for the simulation results;
DATA A; SET &resultsdataset;
PROC SORT; BY NORMAL EQ_VAR;
PROC FREQ; BY NORMAL EQ_VAR;
  TABLES SIG;
RUN;
******************************************************************;

/*** FIFTH RUN: Unequal sample size per group and same variance ***/


%let resultsdataset=sasuser.ANOVA_inpropvar_different_n_30;  *Name of the dataset with the results of the MC experiment;

data meanvar;
 input A B group mean var n;
 datalines;
 1 1 1 50 20 50
 1 1 2 50 20 30
 1 1 3 50 20 10
 1 2 1 50 20 50
 1 2 2 50 20 30
 1 2 3 50 20 10
 2 1 1 50 20 50
 2 1 2 50 20 30
 2 1 3 50 20 10
 2 2 1 50 20 50
 2 2 2 50 20 30
 2 2 3 50 20 10
;
run;

*%ANOVA;       * run macro 'ANOVA';

              * obtain descriptive statistics for the simulation results;
DATA A; SET &resultsdataset;
PROC SORT; BY NORMAL EQ_VAR;
PROC FREQ; BY NORMAL EQ_VAR;
  TABLES SIG;
RUN;
******************************************************************;

/*** SIXTH RUN: Unequal sample size per group and unequal variance ***/


%let resultsdataset=sasuser.ANOVA_inpropvar_different_n_30;  *Name of the dataset with the results of the MC experiment;

data meanvar;
 input A B group mean var n;
 datalines;
 1 1 1 50 20 50
 1 1 2 50 20 30
 1 1 3 50 20 10
 1 2 1 50 20 50
 1 2 2 50 20 30
 1 2 3 50 20 10
 2 1 1 50 20 50
 2 1 2 50 20 30
 2 1 3 50 20 10
 2 2 1 50 20 50
 2 2 2 50 20 30
 2 2 3 50 20 10
;
run;

*%ANOVA;       * run macro 'ANOVA';

              * obtain descriptive statistics for the simulation results;
DATA A; SET &resultsdataset;
PROC SORT; BY NORMAL EQ_VAR;
PROC FREQ; BY NORMAL EQ_VAR;
  TABLES SIG;
RUN;

/*ZAD3*/
/*a */


/*** run jackboot.sas first ***/

   title2 'The unbiased variance estimator is not a plug-in estimator';
   proc means data=sasuser.pills_efron var vardef=df;
   output out=out var=var_x;
      var x;
   run;
/*
The following %ANALYZE macro could be used to jackknife the unbiased
variance estimator, but the bootstrap over-corrects for the nonexistent
bias:
*/
   title2 'Estimating the bias of the unbiased estimator of variance';
   %macro analyze(data=,out=);
      proc means noprint data=&data vardef=df;
         output out=&out(drop=_freq_ _type_) var=var_x;
         var x;
         %bystmt;
      run;
   %mend;

   title3 'The jackknife computes the correct bias of zero';
   %jack(data=sasuser.pills_efron)

   title;



   title2 'The biased variance estimator is not a plug-in estimator';
   proc means data=sasuser.pills_efron var vardef=n;
   output out=out var=var_x;
      var x;
   run;
/*
The following %ANALYZE macro could be used to jackknife the unbiased
variance estimator, but the bootstrap over-corrects for the nonexistent
bias:
*/
   title2 'Estimating the bias of the biased estimator of variance';
   %macro analyze(data=,out=);
      proc means noprint data=&data vardef=n;
         output out=&out(drop=_freq_ _type_) var=var_x;
         var x;
         %bystmt;
      run;
   %mend;
/*3.b nema :( */


/*ZAD4*/
/*4.a nema :(*/
/*b*/
/**neparametarski**/
/** Primjer preuzet iz "268-2010 SUGI Bootstrap.pdf", str.3 (u folderu "Downloaded Papers 2012") **/

/** bootsrtap percentilni 95%CI za korelacijski koeficijent ***/
/*** yourdata= sashelp.cars ***/

sasfile sashelp.cars load; /* 1 */
proc surveyselect data=/*YourData*/sashelp.cars out=outboot /* 2 */
seed=4795 /* 3 */
method=urs /* 4 */
samprate=1 /* 5 */
outhits /* 6 */
rep=100; /* 7 */ /*should be 1000*/
run;

sasfile sashelp.cars close; /* 8 */

ods listing close; /* 9 */
/*ods html close;*/

proc corr data=outboot
out=outall(where=(_type_='CORR' & _name_='length')
                  rename=(weight=corr)
                  keep=weight _TYPE_ _NAME_  );
         var length weight;
by replicate;
run;

ods listing; /* 11 */
/*ods html;*/

proc univariate data=outall;
var corr;
output out=final pctlpts=5, 95 pctlpre=ci_ ;
run;
 
proc print data=final;
run;
