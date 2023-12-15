# Синтаксис языка графических запросов

## Абстрактный синтаксис

```
prog = List<stmt>

stmt =
    Bind of var * expr
  | Print of expr

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Not of expr                  // отрицание
  | And of expr * expr           // логическое и
  | Or expr * expr               // логическое или
  | Set of List<expr>            // создание множества
  | Contain of expr * expr       // contain
  | Set_start of expr * expr     // задать множество стартовых состояний
  | Set_final of expr * expr     // задать множество финальных состояний
  | Add_start of expr * expr     // добавить состояния в множество стартовых
  | Add_final of expr * expr     // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load_dot of path             // загрузка графа из дот файла
  | Load_graph of string         // загрузка графа из базы данных
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)

val =
    String of string                // строчка
  | Int of int                      // целое число
  | Bool of bool                    // логическое значение
  | Regex of srting                 // регулярное выражение
  | Cfg of string                   // контекстно свободная грамматика

pattern =
    Any                                     // отбрасывание значения
  | Name of string                          // именованное значения
  | Unpair of pattern * pattern             // раскрытие пары
  | Untriple of pattern * pattern * pattern // раскрытие тройки

lambda = Lambda of pattern * expr

```

## Грамматика

```
prog -> EOL* (COMMENTS stmt (SPACES COMMENT)? EOL+ )* COMMENTS?

stmt ->
      var SPACES ASSIGN SPACES expr
    | 'print' '(' expr ')'

expr ->
      var
    | val
    | bool
    | set
    | '(' expr ',' SPACES expr ')'
    | '(' expr ',' SPACES expr ',' SPACES expr ')'
    | '(' expr ')'

graph ->
      var
    | REGEX 
    | CFG
    | 'load_dot' '(' (var | SRT) ')'
    | 'load_graph' '(' (var | SRT) ')'
    | graph '.' 'set_start_states' '(' set? ')'
    | graph '.' 'set_finals_states' '(' set? ')'
    | graph '.' 'add_start_states' '(' set ')'
    | graph '.' 'add_final_states' '(' set ')'
    | graph SPACES '&' SPACES graph
    | graph SPACES '^' SPACES graph
    | graph SPACES '|' SPACES graph
    | graph '*'
    | '(' graph ')'

set ->
      var
    | '{' (expr (',' SPACES expr)* )? '}'
    | graph '.' 'get_start_states'
    | graph '.' 'get_final_states '
    | graph '.' 'get_reachables'
    | graph '.' 'get_vertexes'
    | graph '.' 'get_edges'
    | graph '.' 'get_labels'
    | 'map' '(' '{' pattern SPACES '->' SPACES expr '}' SPACES* ',' SPACES set ')'
    | 'filter' '(' '{' pattern SPACES '->' SPACES bool '}' SPACES* ',' SPACES set ')'
    | '(' set ')'

bool ->
      var
    | 'true' 
    | 'false'
    | 'not' SPACES bool
    | bool SPACES '&&' SPACES bool
    | bool SPACES '||' SPACES bool
    | expr SPACES 'in' SPACES expr
    | '(' bool ')'

pattern ->
    '_'
  | var
  | '(' pattern ',' pattern ')'
  | '(' pattern ',' pattern ',' pattern ')'
  
var -> [a-zA-Z_][a-zA-Z_0-9]*

REGEX -> 'r' STR
CFG -> 'g' STR

val -> STR | INT

STR -> '"' ~[\n]* '"'

INT -> '-'? [1-9][0-9]*

COMMENTS -> (COMMENT EOL+ )*
COMMENT -> '#' ~[\n]*

ASSIGN -> '='

EOL -> [\n]+
SPACES -> [ \t]+
```

## Примеры

Получение пар вершин, между которыми существует путь, удовлетворяющий КС-ограничению
```
g = g"S -> a S c | a b";
r = r"a b c"
g_and_r = g & r
res = map({((u, _), (v, _)) -> (u, v)}, g_and_r.get_reachables)
```

Получение всех достижимых вершин из заданного множества
```
g = load_graph("skos").set_start_states({0, 1, 2, 3})
res = map({(_, f) -> f}, g.get_reachables)
```

Получение и печать множества общих меток графов "wine" и "skos"
```
g_w = load_graph("wine")
g_s = load_graph("skos")
print(filter({l -> l in g_w.get_labels)}, g_s.get_labels))
```