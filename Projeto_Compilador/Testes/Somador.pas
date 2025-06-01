program Somador; 
  var 
    num1: integer;
    num2, soma: real;
  begin 
    soma := 0.0;

    Write('Introduza o primeiro número: '); 
    ReadLn(num1);

    Write('Introduza o segundo número: '); 
    ReadLn(num2);

    soma := num1 + num2;

    writeln('A soma dos números é: ', soma); 
  end.