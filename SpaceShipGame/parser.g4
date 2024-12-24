parser grammar SpaceBattleParser;
options { tokenVocab = SpaceBattleLexer; }

game: rules+;

rules
    : canRule
    | canControlRule
    | includeRule
    | predatesRule
    | mustRule
    ;

canRule : ID CAN list_id;

canControlRule: ID CAN_CONTROL list_id;

includeRule : ID INCLUDE list_id;

predatesRule : ID PREDATES list_id;

mustRule: ID MUST ID WHEN ID;

list_id: ID (COMMA ID)* ;

id: ID (OR ID)*;
