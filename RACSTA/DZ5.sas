/*ZAD1*/
%let N = 20;                         /* size of each sample */
%let NumSamples = 1000;              /* number of samples   */  
data SimSK(drop=i);
call streaminit(123);
do SampleID = 1 to &NumSamples;      /* simulation loop             */
   do i = 1 to &N;                   /* N obs in each sample        */
      Normal      = rand("Normal");  /* kurt=0                      */
      t           = rand("t", 5);    /* kurt=6 for t, exp, and logn */
      Exponential = rand("Expo");
      LogNormal   = exp(rand("Normal", 0, 0.503)); 
      output;
   end;
end;
run;

proc means data=SimSK noprint;
   by SampleID;
   var Normal t Exponential LogNormal;
   output out=Moments(drop=_type_ _freq_) Kurtosis=;
run;

proc transpose data=Moments out=Long(rename=(col1=Kurtosis));
   by SampleID;
run;

proc sgplot data=Long;
   title "Kurtosis Bias in Small Samples: N=&N";
   label _Name_ = "Distribution";
   vbox Kurtosis / category=_Name_ meanattrs=(symbol=Diamond);
   refline 0 6 / axis=y;
   yaxis max=30;
   xaxis discreteorder=DATA;
run;

/* bias/pristranost koeficijenta splotenosti (kurtosis) za male uzorke */
%let N = 100;                         /* size of each sample */
%let NumSamples = 1000;              /* number of samples   */  
data SimSK(drop=i);
call streaminit(123);
do SampleID = 1 to &NumSamples;      /* simulation loop             */
   do i = 1 to &N;                   /* N obs in each sample        */
      Normal      = rand("Normal");
      t           = rand("t", 5);   
      Exponential = rand("Expo");
      LogNormal   = exp(rand("Normal", 0, 0.503)); 
      output;
   end;
end;
run;

proc means data=SimSK noprint;
   by SampleID;
   var Normal t Exponential LogNormal;
   output out=Moments(drop=_type_ _freq_) Kurtosis=;
run;

proc transpose data=Moments out=Long(rename=(col1=Kurtosis));
   by SampleID;
run;

proc sgplot data=Long;
   title "Kurtosis Bias in Small Samples: N=&N";
   label _Name_ = "Distribution";
   vbox Kurtosis / category=_Name_ meanattrs=(symbol=Diamond);
   refline 0 6 / axis=y;
   yaxis max=30;
   xaxis discreteorder=DATA;
run;
/*ZAD2*/
* 5.1.;
%let N = 50;
%let NumSamples = 1000;
%let SeedValue = 0; /* Set the seed value to 0 */

/* Run simulation with 0 as the seed value for 10 iterations */
%macro run_sim(seed);
    data Normal(keep=SampleID x);
        call streaminit(&seed);
        do SampleID = 1 to &NumSamples;
            do i = 1 to &N;
                x = rand("Normal");
                output;
            end;
        end;
    run;

    proc means data=Normal noprint;
        by SampleID;
        var x;
        output out=OutStats mean=SampleMean lclm=Lower uclm=Upper;
    run;

    data OutStats; set OutStats;
        ParamInCI = (Lower<0 & Upper>0);
    run;

    proc freq data=OutStats;
        tables ParamInCI / nocum;
        ods output onewayfreqs=Freqs;
    run;
%mend;

/* Call the macro 10 times with the same seed value */
data Results;
    do i = 1 to 10;
        call execute('%run_sim(' || strip(&SeedValue) || ');'); /* Use the &SeedValue macro variable */
        output;
    end;
run;

*5.3.;
%let N = 50;
%let NumSamples = 10000;
/* 1. Simulate obs from N(0,1) and Exp(1) - 1 */
data Exp(keep=SampleID x);
call streaminit(123);
do SampleID = 1 to &NumSamples;
    do i = 1 to &N;
        x = rand("Expo") - 1;
        output Exp;
    end;
end;
run;

/* 2. Compute statistics for each sample */
proc means data=Normal noprint;
by SampleID;
var x;
output out=OutStats mean=SampleMean lclm=Lower uclm=Upper;
run;

/* how many CIs include parameter? */
data OutStats; set OutStats;
ParamInCI = (Lower<0 & Upper>0);
NotParamInCI = 1 - ParamInCI; /* variable of interest */
run;

/* Nominal coverage probability is 95%. Estimate true coverage. */
proc freq data=OutStats;
tables NotParamInCI / binomial (p=0.95);
run;


/*ZAD3*/
*5.6;
/* test sensitivity of t test to equal variances */
%let n1 = 10;
%let n2 = 10;
%let NumSamples = 10000;
/* number of samples
*/
/* Scenario 1: (x1 | c=2) ~ N(0,2);
*/
/* Scenario 2: (x2 | c=2) ~ N(0,5);
*/
/* Scenario 3: (x2 | c=2) ~ N(0,100);
*/
data EV(drop=i);
label x1 = "Normal data, same variance"
x2 = "Normal data, different variance"
x3 = "Normal data, different variance";
call streaminit(321);
do SampleID = 1 to &NumSamples;
c = 2;
/* sample from second group */
do i = 1 to &n2;
x1 = rand("Normal", 0, 2);
x2 = rand("Normal", 0, 5);
x3 = rand("Normal", 0, 100);
output;
end;
end;
run;



*5.7;
/* test sensitivity of t test to equal variances */
%let n1 = 10;
%let n2 = 10;
%let NumSamples = 10000;
/* number of samples
*/
/* Scenario 1: (x1 | c=1) ~ N(0,1); (x1 | c=2) ~ N(0,1);
*/
/* Scenario 2: (x2 | c=1) ~ N(0,1); (x2 | c=2) ~ N(0,10);
*/
data EV(drop=i);
label x1 = "Normal data, same variance"
x2 = "Normal data, different variance";
call streaminit(321);
do SampleID = 1 to &NumSamples;
c = 1;
/* sample from first group */
do i = 1 to &n1;
x1 = rand("Gamma", 10);
x2 = 10 * rand("Exponential");
output;
end;
c = 2;
/* sample from second group */
do i = 1 to &n2;
x1 = rand("Gamma", 10);
x2 = 10 * rand("Exponential");
output;
end;
end;
run;

/*ZAD4*/
*5.8;
/* test sensitivity of t test to equal variances */
%let n1 = 10;
%let n2 = 10;
%let NumSamples = 10000;
/* number of samples
*/
/* Scenario 1: (x1 | c=1) ~ N(0,1); (x1 | c=2) ~ N(0,1);
*/
/* Scenario 2: (x2 | c=1) ~ N(0,1); (x2 | c=2) ~ N(0,10);
*/
data EV(drop=i);
label x1 = "Normal data, same variance"
x2 = "Normal data, different variance";
call streaminit(321);
do SampleID = 1 to &NumSamples;
c = 1;
/* sample from first group */
do i = 1 to &n1;
x1 = rand("Gamma", 10);
x2 = 10 * rand("Exponential");
output;
end;
c = 2;
/* sample from second group */
do i = 1 to &n2;
x1 = rand("Gamma", 10);
x2 = 10 * rand("Exponential");
output;
end;
end;
run;



/*ZAD5*/

*11.2.;
/* Technique 2: Put simulation loop inside loop over observations */
data RegSim2(keep= SampleID i x y);
call streaminit(1);
do i = 1 to &N;
x = rand("Uniform");
/* use this value NumSamples times */
eta = 1 - 2*x;
/* parameters are 1 and -2
*/
do SampleID = 1 to &NumSamples;
y = eta + rand("Normal", 0, 0.5);
output;
end;
end;
run;
proc sort data=RegSim2;
by SampleID i;
run;

proc reg data=RegSim2 outest=OutEst NOPRINT;
by SampleID;
model y = x;
quit;
ods graphics on;
proc corr data=OutEst noprob plots=scatter(alpha=.05 .1 .25 .50);
label x="Estimated Coefficient of x"
Intercept="Estimated Intercept";
var Intercept x;
ods exclude VarInformation;
run;

/* Analyze RMSE estimates */
proc univariate data=OutEst;
var _RMSE_;
histogram / normal(mu=est sigma=est);
run;

/* Test normality of ASD */
proc univariate data=OutEst;
var _RMSE_;
qqplot _RMSE_ / normal(mu=est sigma=est);
run;
