/*DZ4 ZRINKA PECANIC 0036517187*/

/*ZAD1*/

/*ZAD2*/

/*ZAD3*/
data UCINKOVITOST;
         input formulacija minute @@;
         datalines;
      1 1.96   1 1.94   1 2.92   1 2.90   1 2.96   1 3.27
      1 3.25   1 3.27   1 3.27   2 3.70   2 3.74
      2 3.28   2 3.27   2 3.30   2 3.71   2 3.72   
      ;
run;



/*ZAD4*/
%let NumSamples = 1000; 
/* Simulate data */
data SimUniSize;
call streaminit(123);
do N = 10 to 200 by 10;
    do SampleID = 1 to &NumSamples;
        do i = 1 to N;
            x = rand("Uniform");
            output;
        end;
    end;
end;
run;

/* Compute mean and standard error*/
proc means data=SimUniSize noprint;
    by N SampleID;
    var x;
    output out=OutStats mean=SampleMean stderr=SampleSE;
run;

/*Summarize standard error*/
proc means data=OutStats mean;
    class N;
    var SampleSE;
    output out=StdErrMeans mean=SEmean;
run;

/* Plot standard error of mean as a function of sample size */
/* title "Standard Error of Mean vs. Sample Size";
proc sgplot data=StdErrMeans;
    scatter x=N y=SampleSE / markerattrs=(symbol=circlefilled size=8);
    series x=N y=SEmean / lineattrs=(pattern=dot thickness=2);
    xaxis label="Sample Size";
    yaxis label="Standard Error of Mean";
run; */


/*ZAD5*/

/* bias of kurtosis in small samples */
%let N = 50; 
%let NumSamples = 1000; 
data SimSK(drop=i);
call streaminit(123);
do SampleID = 1 to &NumSamples; 
	do i = 1 to &N; 
		Normal = rand("Normal"); 
		t = rand("t", 5); 
		Exponential = rand("Expo");
		LogNormal = exp(rand("Normal", 0, 0.503));
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


%let N = 2000; 
%let NumSamples = 1000; 
data SimSK(drop=i);
call streaminit(123);
do SampleID = 1 to &NumSamples; 
	do i = 1 to &N; 
		Normal = rand("Normal"); 
		t = rand("t", 5); 
		Exponential = rand("Expo");
		LogNormal = exp(rand("Normal", 0, 0.503));
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