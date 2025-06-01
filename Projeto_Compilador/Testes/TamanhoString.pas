program TamanhoString; 
var 
  palavra: string;
  tamanho: integer; 
begin 
  tamanho := 0;
  writeln('Introduza uma palavra:'); 
  readln(palavra); 
  tamanho :=  length(palavra);
  writeln('O tamanho da palavra é: ', tamanho); 
end.