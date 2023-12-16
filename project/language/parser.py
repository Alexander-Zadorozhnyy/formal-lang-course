from antlr4 import (
    CommonTokenStream,
    InputStream,
    ParseTreeWalker,
    ParserRuleContext,
    TerminalNode,
)
import pydot


from project.language.GraphLangLexer import GraphLangLexer
from project.language.GraphLangParser import GraphLangParser
from project.language.GraphLangListener import GraphLangListener


def parse_to_ast(text: str) -> GraphLangParser:
    stream = InputStream(text)
    lexer = GraphLangLexer(stream)
    tokens = CommonTokenStream(lexer)

    return GraphLangParser(tokens)


def check_ast(text: str) -> bool:
    parser = parse_to_ast(text)
    parser.removeErrorListeners()
    program = parser.prog()

    listener = IsRightTreeListener()
    walker = ParseTreeWalker()

    try:
        walker.walk(listener, program)
        return parser.getNumberOfSyntaxErrors() == 0
    except ValueError:
        return False


def save_to_dot(parser: GraphLangParser, path: str):
    tree = parser.prog()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise ValueError("Something went wrong! Parsing isn't work correctly!")

    listener = DotTreeListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    if not listener.dot.write(path):
        raise RuntimeError(f"Can't save to {path} file! Try again!")


class IsRightTreeListener(GraphLangListener):
    def __init__(self):
        self.is_sub_tree = False

    def enterEveryRule(self, contex: ParserRuleContext):
        self.is_sub_tree = False

    def exitEveryRule(self, contex: ParserRuleContext):
        if not self.is_sub_tree:
            raise ValueError("Parser has syntax errors")

    def visitTerminal(self, node: TerminalNode):
        self.is_sub_tree = True


class DotTreeListener(GraphLangListener):
    def __init__(self):
        self.dot = pydot.Dot("ast", strict=True)
        self.curr = 0
        self.stack = []

    def enterEveryRule(self, ctx: ParserRuleContext):
        self.dot.add_node(
            pydot.Node(self.curr, label=GraphLangParser.ruleNames[ctx.getRuleIndex()])
        )

        if len(self.stack) > 0:
            self.dot.add_edge(pydot.Edge(self.stack[-1], self.curr))

        self.stack += [self.curr]
        self.curr += 1

    def exitEveryRule(self, ctx: ParserRuleContext):
        self.stack.pop()

    def visitTerminal(self, node: TerminalNode):
        self.dot.add_node(pydot.Node(self.curr, label=f"'{node}'", shape="box"))
        self.dot.add_edge(pydot.Edge(self.stack[-1], self.curr))
        self.curr += 1
