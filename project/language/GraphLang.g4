grammar GraphLang;

//prog : EOL* (COMMENTS stmt (SPACES COMMENT)? EOL+ )* COMMENTS? ;
//prog : EOL* (COMMENTS stmt (SPACES COMMENT)? EOL+)* (stmt COMMENT?)? EOF;
prog : EOL* ((COMMENT EOL+)* stmt EOL+)* (stmt COMMENT?)? EOF;

stmt :
      PRINT LP expr RP
    | VAR ASSIGN expr
    ;

expr :
    | VAR
    | INT
    | STR
    | BOOL
    | REGEX
    | CFG
    | NOT expr
    | expr DOT SET_START_STATES LP expr RP
    | expr DOT SET_FINAL_STATES LP expr RP
    | expr DOT ADD_START_STATES LP expr RP
    | expr DOT ADD_FINAL_STATES LP expr RP
    | expr DOT GET_START_STATES
    | expr DOT GET_FINAL_STATES
    | expr DOT GET_REACHABLES
    | expr DOT GET_VERTEXES
    | expr DOT GET_EDGES
    | expr DOT GET_LABELS
    | MAP LP LC pattern ARROW expr RC  COMMA expr RP
    | FILTER LP LC pattern ARROW expr RC  COMMA expr RP
    | LOAD_DOT LP (VAR | STR) RP
    | LOAD_GRAPH LP (VAR | STR) RP
    | LP expr  COMMA expr RP
    | LP expr  COMMA expr  COMMA expr RP
    | expr AMPER expr
    | expr CARET expr
    | expr PIPE expr
    | expr ASTER
    | expr IN expr
    | LC RC
    | LC (expr ( COMMA expr)* )? RC
    | LP expr RP
    ;


pattern :
    ANY
  | VAR
  | LP pattern  COMMA pattern RP
  | LP pattern  COMMA pattern  COMMA pattern RP
  ;

// Main graph utils

LOAD_DOT : 'load_dot';
LOAD_GRAPH : 'load_graph';

SET_START_STATES : 'set_start_states';
SET_FINAL_STATES : 'set_final_states';
ADD_START_STATES : 'add_start_states';
ADD_FINAL_STATES : 'add_final_states';

GET_START_STATES : 'get_start_states';
GET_FINAL_STATES : 'get_final_states';
GET_REACHABLES : 'get_reachables';
GET_VERTEXES : 'get_vertexes';
GET_EDGES : 'get_edges' ;
GET_LABELS : 'get_labels';

// Hepler set functions

MAP : 'map';
FILTER : 'filter';

// Operations

AMPER : '&';
PIPE : '|';
CARET : '^';
ASTER : '*';

OR : '||';
AND : '&&';

NOT : 'not';

ASSIGN : '=';
IN : 'in';

// Lambda
ARROW : '->';

// Brackets

LP : '(';
RP : ')';
LC : '{';
RC : '}';

// Utils

PRINT : 'print';

COMMA : ',';
DOT : '.';
ANY : '_';

SPACES : [ \t\r]+ -> skip;
EOL : '\n';

// Types

VAR : [a-zA-Z_][a-zA-Z0-9_]*;
STR : '"' ~[\n]* '"';
INT : '0' | '-'? [1-9][0-9]*;
BOOL : 'true' | 'false';
REGEX : 'r' STR;
CFG : 'g' STR;

// Comments
COMMENT : '#' ~[\n]* -> skip;
