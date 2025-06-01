program NegativoOuMaiorQue100;
var
  num: integer;
begin
  writeln('Digite um número:');
  readln(num);
  if (num < 0) or (num > 100) then
    writeln('O número é negativo ou maior que 100.')
  else
    writeln('O número está entre 0 e 100.');
end.
