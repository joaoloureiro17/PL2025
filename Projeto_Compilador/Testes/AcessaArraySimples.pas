program AcessaArraySimples;

var
  arr: array[0..4] of integer;
  i: integer;

begin
  arr[0] := 10;
  arr[1] := 20;
  arr[2] := 30;
  arr[3] := 40;
  arr[4] := 50;

  readln(i);
  writeln(arr[i]);
end.