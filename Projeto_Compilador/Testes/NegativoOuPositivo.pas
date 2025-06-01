program ExemploOperadorNOT;
var
  numero: integer;
  resultado: boolean;
begin
  writeln('Digite um numero inteiro:');
  readln(numero);
  
  { Verifica se o número é positivo ou negativo }
  resultado := not (numero >= 0);

  if resultado then
    writeln('O numero ', numero, ' é negativo.')
  else
    writeln('O numero ', numero, ' é positivo ou zero.');
end.
