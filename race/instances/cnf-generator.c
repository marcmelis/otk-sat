/* Program for generating random instances of SAT problems.   */
/* This program is written by Bart Selman. It is property     */
/* of AT&T. For research use only.                            */
/*     Copyright 1992 by AT&T Bell Laboratories               */
/*     All Rights Reserved                                    */
/* AT&T disclaims all warranties with regard to this software,    */
/* including all implied warranties of merchantability and        */
/* fitness.  In no event shall AT&T be liable for any special,    */
/* indirect or consequential damages or any damages whatsoever    */
/* resulting from loss of use, data or profits, whether in an     */
/* action of contract, negligence or other tortious action,       */
/* arising out of or in connection with the use or performance of */
/* this software.                                                 */

/* Modified by Jordi Planes to deal with weighted CNF, p-CNF by Nov. 2004 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include <string.h>
#include <libgen.h>


#define LINE_LENGTH 10
#define MAXLINE 60     /* max number char for fgets function */
#define MAX_LINES 25   /* max num output lines per print func */  
#define MAX_LINES_CLAUSES 10 /* max num clauses from wff printed */
#define MAX_BAD_CLAUSES 25 /* max number printed */
#define PRINT_BRANCH 1 /* printing after PRINT_BRANCH branches */
#define MAX_PSAT 10 /* max number of divisions in p-sat */
#define MAX_WEIGHT 10 /* max weight that can be given */
#define TRUE 1
#define FALSE 0

//long random();              /*used functions                                 */
//long srandom();
double fabs();
double floor();

/* Modul functions */
void init_rand();
void init_assign_values();
void init_clause_values();
void clear_clause();
void make_clause(int,int,int);
int store_clause(int);
void output_wff(char*);
int not_in_clause(int);
void print_clause(void);
int get_clause(int,int);
int local_in_clause(int,int);
int clause_sat();

double BIG = 017777777777l;   /* 2**31 -1                              */

typedef struct lit_str {
  int lit;
  int next;
  int next_save;       /* permanent copy */
  int lits_remain;     /* num lits remaining */
  int lits_remain_save;/* permanent copy */ 
} *lit_str_ptr;        /* lit_str_ptr is a pointer to structure lit_str */

typedef struct var_str {
  int name;
  short int value;
  int make;
  int critical;
  int diff;
  int first;
  int first_save;      /* permanent copy */
  int max_diff_list;      
  int forced;          /* 1 if forced by propagation */
  int local;           /* 1 if clauses are localized */
  int local_length;    /* window of vars to pick from */
  int picked;          /* 1 if value of variable has been set in choices */
} *var_str_ptr;        

typedef struct choices_str {
  int value;
} *choices_str_ptr;

typedef struct forced_str {
  int value;
} *forced_str_ptr;

typedef struct prop_array_str{
  int value;
} *prop_array_str_ptr;

typedef struct cl_lit_str {
  short int lit;
  int pos;
} *cl_lit_str_ptr;        /* cl_lit_str_ptr is a pointer to structure 
                             cl_lit_str; use to hold temp clause */

lit_str_ptr wff;       /* wff is global array containing the wff 
                          first lit at location 0 */
var_str_ptr assign;    /* assign is global array containing the assignment
                          variable name from 1 to N stored atlocations 1 to N */
choices_str_ptr choices; /* list of (unforced) dp choices made 
                          from 1 to N ; first entry is count */
forced_str_ptr forced; /* list of forced (by propagation) dp choices made 
                          from 1 to N ; first entry is count */
prop_array_str_ptr prop_array; /* branch of dp */ 
                       /* from 1 to N ; first entry is count */
cl_lit_str_ptr clause; /* clause is global array containing a clause 
                          length in location 0 first lit at location 1 */

unsigned int nvars,     /* number of variables */
             nclauses,  /* number of clauses */
             nlits,     /* number of literals  */
             clause_length, /* number of lits per clause */
             psat,      /* number of random p-sat */
             weight;    /* clause weighting */

char weighted_cnf;

int gsat_max_steps,  /* max number of flips per try */
    gsat_max_tries,  /* max number of tries from random state */
    gsat_num_exp;    /* total number of experiments */

int crit_bad_clauses, /* when to start boosting */
    additional_steps, /* number additional flips during boosting */

    downwards_count,   /* counting max_diff > 0  -- total count for each try */
    sideways_count,    /* counting max_diff = 0  -- total count for each try */
    upwards_count,     /* counting max_diff < 0  -- total count for each try */
    flag_down_only,    /* if 1 then only downwards moves */
   
    clauses_sat,       /* counts number of satisfied clauses so far */
    num_nodes,         /* total number of nodes in DP tree */
    num_bin_nodes,     /* total number of binary nodes in DP tree */
    num_unary_nodes,   /* total number of unary nodes in DP tree */
    num_branches;      /* total number of branches in DP tree */

/* The main routine. */
int main ( int argc, char *argv[] ) {
     char wff_file[MAXLINE];
     int i, t;
     int forced, last_lit, local, local_length;
     int times = 1;
     char weight_cnf[2] = {'\0', '\0'};

     psat = MAX_PSAT;
     weighted_cnf = 0;

     if ( strcmp( basename( *argv ), "cnf-rand-pgenerator" ) == 0 ) {
       if ( argc < 6 ) {
	 printf("usage: cnf-rand-pgenerator times psat c-length variables clauses\n");
	 printf("       with psat = 5 and c-length = 2 will generate clauses of length 2 and 3 with equal probability\n");
	 exit(-1);
       }

       argv++;
       times = atoi( *argv++ );
       psat = atoi( *argv++ );
     }
     if ( strcmp( basename( *argv ), "cnf-rand-generator" ) == 0 ) {
       if ( argc < 5 ) {
	 printf("usage: cnf-rand-generator times c-length variables clauses\n");
	 exit(-1);
       }

       argv++;
       times = atoi( *argv++ );
     }
     if ( strcmp( basename( *argv ), "cnf-rand-wgenerator" ) == 0 ) {
       if ( argc < 5 ) {
	 printf("usage: cnf-rand-wgenerator times c-length variables clauses\n");
	 exit(-1);
       }
       argv++;
       times = atoi( *argv++ );
       weighted_cnf = 1; printf("Assignem pes\n");
       strcpy( weight_cnf, "w" );
     }
     
     if ( argc < 5 ) {
       printf("usage: cnf-generator c-length variables clauses\n");
       exit(-1);
     }

     setbuf(stdout,NULL);
     printf(" program: wff ");
     /* give name of file with wff */

     //strcpy( wff_file, *argv++ );
     /*
     scanf("%s", wff_file);
     */
     //fgets(wff_file, MAXLINE, stdin);
     //printf("\n wff_file: %s", wff_file);
     /*
     printf("\n forced? (1): ");
     scanf("%d", &yn);
     */     
     forced = 0;
     /*
     if (yn == 1) forced = 1;
     if (forced == 1) 
        printf("\n forced sat ");
     else
        printf("\n not forced ");
     */
     local = 0;
     local_length = 1;
     
     /* initializes rand #s */
     init_rand();    

     /*
     printf("\n clause_length: ");
     scanf("%d", &clause_length);
     printf(" nvars: ");
     scanf("%d", &nvars);
     printf(" nclauses: ");
     scanf("%d", &nclauses);
     */
     clause_length = atoi( *argv++ );
     nvars = atoi( *argv++ );
     nclauses = atoi( *argv );
     printf("\n clause_length: %d  nvars: %d  nclauses: %d ", clause_length, 
	    nvars, nclauses);

     for( t = 0; t < times; t++ ) {

       if ( psat < MAX_PSAT ) {
	 sprintf( wff_file, "s%dv%dc%dp%d-%d.%scnf", clause_length, nvars, nclauses, 
		  psat, t+1, weight_cnf);
       }
       else {
	 sprintf( wff_file, "s%dv%dc%d-%d.%scnf", clause_length, nvars, nclauses, t+1, weight_cnf);
       }
       
       printf("\nfile: %s\n", wff_file);
       
       /* allocate memory for the wff */
       nlits = nclauses * clause_length;
       wff = (lit_str_ptr) malloc (nlits*clause_length * (sizeof(struct lit_str)));
       /* allocate memory for the assignment */
       assign = (var_str_ptr) malloc ((nvars + 1) * (sizeof(struct var_str)));
       /* allocate memory for temporary storage of a clause */
       clause = (cl_lit_str_ptr) malloc ((nvars + 1) * 
					 (sizeof(struct cl_lit_str)));
       init_assign_values();
       init_clause_values();

       //printf("\n init done ");
       last_lit = -1;
       for (i = 1; i <= nclauses; i++) {
         clear_clause();
         make_clause(forced, local, local_length);
         last_lit = store_clause(last_lit);
       }
       output_wff(wff_file);
       //printf(" \n done \n ");
       
     }
     return 0;
}

void init_assign_values()     /* initializes assigns values randomly */
{
       int i;
          /* initialize assign */
          for (i = 0; i <= nvars; i++){
              if ( (((double) random() / BIG) -0.5) > 0.0 ) {
                   assign[i].value = 1;}
              else {
                   assign[i].value = -1;}
              assign[i].make = 0;
              assign[i].critical = 0;
              assign[i].diff = 0;
              }
}

void init_clause_values()     /* initializes clause entries to 0 */
{
       int i;
          for (i = 0; i <= nvars; i++)
                   clause[i].lit = 0;
}

void clear_clause()
{
       int i;
          for (i = 0; i <= clause_length; i++)
                   clause[i].lit = 0;
}

void print_wff(){
     int i;
     printf("\n wff: ");
     for (i = 0; i < nlits; i++) {
        printf("\n %4d %4d %4d", i, wff[i].lit, wff[i].next);
        if (i > MAX_LINES) break;}
     printf("\n ");
}

void print_wff_clauses(){
      int i, pntr, tmp;
      printf("\n clauses: ");
      pntr = 0;
      for (i = 1; i <= nclauses; i++){
          if (i >= MAX_LINES_CLAUSES) break;
          tmp = get_clause(pntr,1);
          print_clause();
          pntr = pntr + clause[0].lit;
          }
      printf("\n");
      }

void output_wff( char *wff_file )
{
      int i, j, pntr, tmp;

      FILE  *fopen(), *fp = fopen(wff_file, "w");

      if ( weighted_cnf ) fprintf(fp,"c Weighted CNF\n");
      else fprintf(fp, "c CNF\n");

      if ( weighted_cnf ) 
	fprintf(fp,"c from Selman's wff generator\np wcnf %d  %d\n",nvars, nclauses); 
      else
	fprintf(fp,"c from Selman's wff generator\np cnf %d  %d\n",nvars, nclauses); 

      pntr = 0;
      for (i = 1; i <= nclauses; i++){
          tmp = get_clause(pntr,1);
          /* fprintf(fp,"\n%d  ", clause[0].lit); */
          //fprintf(fp,"( ");	  
	  if ( weighted_cnf ) {
	    fprintf(fp,"%d ", weight);
	  }	  
          for (j = 1; j <= clause[0].lit; j++) {
	    if ( abs( clause[j].lit ) != nvars + 2) { // lit == nvars + 2 when the literal is cancelled
	      fprintf(fp,"%d ", clause[j].lit);	      
	    }
	  }
          fprintf(fp,"0\n");
          pntr = pntr + clause[0].lit;
      }
      //fprintf(fp,"%%\n0\n");
      //fprintf(fp,"\n");
      fclose(fp);
}

int store_clause(last_lit) /* returns position of last lit in wff array */  
int last_lit;
{
      int i,lit;

      /* first lit is oversized */
      lit = clause[1].lit;
      if (lit > 0 )
         wff[(last_lit + 1)].lit = lit + nvars;
      else
         wff[(last_lit + 1)].lit = lit - nvars;

      for (i = 2; i<=clause[0].lit; i++)
         wff[(last_lit + i)].lit = clause[i].lit;

      return (last_lit + clause[0].lit);
}

          /* initialize assign */

void make_clause(forced, local, local_length) /* generate random clause */
int forced, local, local_length;    
                      /* if forced == 1 then satsifiable by 1 1 1 ... assign. */
                      /* if local == 1 then localize clause. */
{
  int i, var;
     
     clause[0].lit = 0;
     for (i = 1; i <= clause_length; i++) {
       /* pick var not yet in clause */
       while ( 1 == 1 ) {
         var = floor(((double) random() / BIG) * nvars);
         ++var;
         if (var == (nvars + 1) ) --var;
         if ((var <= 0) || (var > nvars)) {
	   printf("ERROR!!");
	   exit(-1);}
         if ( (not_in_clause(var) == 1) &&
              ((local_in_clause(var, local_length) == 1) || (local != 1))) break;
       }
       clause[i].lit = var;
       clause[0].lit++;
     }
     
     if ( psat < MAX_PSAT ) {
       if ( floor(((double)random() / BIG) * MAX_PSAT) >= psat ) {
	 clause[1].lit = nvars + 2; /* the literal will be removed */
       }
     }
     
     while ( 1 == 1) {
       for (i = 1; i <= clause_length; i++)
	 /* set random sign */
	 if ( (((double) random() / BIG) -0.5) > 0.0 ) 
	   clause[i].lit = (-1 * clause[i].lit);
       if ((forced != 1) || (clause_sat() == 1))
	 break;
     }
}

int not_in_clause(var)  /* 1 if not in; otherwise 0 */
int var;
{
    int i;
    for (i = 1; i <= clause[0].lit; i++)
        if (abs(clause[i].lit) == var) return 0;
    return 1;
}

int local_in_clause(var, local_length) /* 1 if var is local; otherwise 0 */
int var, local_length;
{
    int i;
    for (i = 1; i <= clause[0].lit; i++)
        if (abs(abs(clause[i].lit) - var) > local_length) return 0;
    return 1;
}

void init_rand()  /* create more random bits */
{
  struct timeval tv;
  struct timezone tzp;
  int sec, seed, n;
  n = gettimeofday(&tv,&tzp);
  sec = (int) tv.tv_sec;
  printf(" \n sec: %d", sec);
  seed = sec * 1000000 + (int) tv.tv_usec;
  srandom(seed);
  printf(" \n rand seed: %10d", seed);
}

int get_bad_clauses(pr)   /* returns number of unsat clauses */
int pr;
{
      int count_bad, tmp, count;

      count_bad = 0;
      count = 0;
      if (pr == 1) printf("\n BAD_CLAUSES: ");
      while (count < nlits)  {
         tmp = get_clause(count,1);
         /* print_clause(); */
         if (clause_sat() == 0) {
            count_bad++;
            if (count_bad <= MAX_BAD_CLAUSES) {
               if (pr == 1) print_clause(); 
               }
            }
         count = count + clause[0].lit;
         }
      return count_bad;
}

void print_clause(){
     int i;
     printf("\n  %2d  ", clause[0].lit);
     for (i = 1; i <= clause[0].lit; i++)
        printf(" %d ", clause[i].lit);
}

int clause_sat() /* returns 1 if satisfied 0 otherwise */
{
      int i;
      for (i = 1; i <= clause[0].lit; i++) {
          if ( assign[abs(clause[i].lit)].value * clause[i].lit > 0 )
             return 1;
          }
      return 0;
}

int get_clause(ptr,var)   /* gets clause and returns pointer to next one */
int ptr, var;             /* that contains var                           */
{
      int lit,ptr_next,len_clause;

      if ( weighted_cnf ) {
	weight = floor(((double) random() / BIG) * MAX_WEIGHT ) + 1;
      }

      ptr_next = 0;
      len_clause = 0;
      lit = wff[ptr].lit;
      /* first lit is oversized */
      lit = lit - ((lit / abs(lit)) * nvars);
      if (abs(lit) == var) ptr_next = wff[ptr].next;
      ++len_clause;
      clause[len_clause].lit = lit;
      ++ptr;
      if (ptr == nlits) {
              clause[0].lit = len_clause;
              return ptr_next;
              }
      lit = wff[ptr].lit;
      if (abs(lit) == var) ptr_next = wff[ptr].next;
      while (abs(lit) <= nvars){
         ++len_clause;
         clause[len_clause].lit = lit;
         ++ptr;
         if (ptr == nlits) {
              clause[0].lit = len_clause;
              return ptr_next;
              }
         lit = wff[ptr].lit;
         if (abs(lit) == var) ptr_next = wff[ptr].next;
         }
      clause[0].lit = len_clause;
      return ptr_next;
}





