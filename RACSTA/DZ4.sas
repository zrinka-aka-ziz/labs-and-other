/*DZ4 ZRINKA PECANIC 0036517187*/

/*ZAD1*/

/* Iman-Conover method - generate MV data with known marginals
and rank correlation */
proc iml;
start ImanConoverTransform(Y, C);
	X = Y;
	N = nrow(X);
	R = J(N, ncol(X));
	/* compute scores for each column */
	do i = 1 to ncol(X);
		h = quantile("Normal", rank(X[,i])/(N+1) );
		R[,i] = h;
	end;
	
	Q = root(corr(R));
	P = root(C);
	S = solve(Q,P); /* equal to S = inv(Q) * P; */
	M = R*S;
	do i = 1 to ncol(M);
		rank = rank(M[,i]);
		y = X[,i];
		call sort(y);
		X[,i] = y[rank];
	end;
	return( X );
finish;

/* Specify marginal distributions */
call randseed(1);
N = 100;
A = j(N,4); y = j(N,1);
distrib = {"Normal" "Lognormal" "Expo" "Uniform"};
do i = 1 to ncol(distrib);
    call randgen(y, distrib[i]);
    A[,i] = y;
end;

/* Specify target rank correlation */
C = { 1.00 0.75 -0.70 0,
      0.75 1.00 -0.95 0,
     -0.70 -0.95 1.00 -0.2,
      0    0   -0.2  1.0};

/* Generate Sim data set */
X = ImanConoverTransform(A, C);

/* Write Sim data set */
create Sim from X[c=("x1":"x4")];
append from X;
close Sim;

/* Compute Spearman correlations*/
proc corr data=Sim fisher plots=matrix(hist);
    var x1-x4;
run;


/*ZAD2*/

/* load SASHELP.CARS */
data work.cars;
   set sashelp.cars;
run;

/* Def vars*/
data CARSDATA;
   set work.cars;
   keep INVOICE MPG_City WEIGHT;
run;

/* a */

proc copula data=CARSDATA;
   var INVOICE MPG_City WEIGHT;
   fit normal;
   simulate / seed=111  ndraws=100
              marginals=empirical  outuniform=UnifData;
run;

/* inv cummulative funcs */
data SIM;
   set UNIFDATA;
   INVOICE_inv = quantile("exponential", INVOICE);
   MPG_City_inv = quantile("lognormal", MPG_City);
   WEIGHT_inv = quantile("lognormal", WEIGHT);
run;


proc corr data=CARSDATa;      
   var INVOICE MPG_City WEIGHT;
run;

proc corr data=SIM;      
   var INVOICE MPG_City WEIGHT;
run;



/*ZAD3*/


%let N = 50;                         /* sample size */
%let NumSamples = 2000;              /* num of samples   */
%let SEED = 5588;                    

data SimSK(drop=i);
   call streaminit(&SEED);
   do SampleID = 1 to &NumSamples;      /* simulation            */
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
   output out=Moments(drop=_type_ _freq_) Skewness=;
run;

proc transpose data=Moments out=Long(rename=(col1=Skewness));
   by SampleID;
run;

proc sgplot data=Long;
   title "Skewness Bias in Small Samples: N=&N";
   label _Name_ = "Distribution";
   vbox Skewness / category=_Name_ meanattrs=(symbol=Diamond);
   refline 0 2 1.764 / axis=y;
   yaxis max=3;
   xaxis discreteorder=DATA;
run;
