lexer grammar SpaceBattleLexer;

CAN: 'can';
CAN_CONTROL: 'can control';
INCLUDE: 'include';
PREDATES: 'predates';
MUST : 'must';
WHEN : 'when' ;
OR: 'or';

COMMA: ',';

ID: [a-zA-Z_][a-zA-Z_0-9]*;
WS: [ \t\n\r\f]+ -> skip ;
