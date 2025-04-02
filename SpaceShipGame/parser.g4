parser grammar SpaceBattleParser;
options { tokenVocab = SpaceBattleLexer; }

game: entity+ ;

entity: statement+ ;

statement
    : canRule
    | canControlRule
    | includeRule
    | orderingRule
    | mustRule
    ;

canRule: ID CAN idListComma ;
canControlRule: ID CAN_CONTROL idListComma ;
includeRule: ID INCLUDE idListComma ;

orderingRule: ID orderingKeyword idListComma ;

orderingKeyword: PREDATES | PRECEDES ;

mustRule: ID MUST ID WHEN idListOr ;

idListComma: ID (COMMA ID)* ;
idListOr: ID (OR ID)* ;
