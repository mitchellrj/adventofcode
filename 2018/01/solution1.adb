with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

type Frequency is Integer

procedure One is
begin
    ResultFrequency  : Frequency := 0;
    CurrentFrequency : Frequency := 0;
    Pos : Postive_Count;
    InputFile : File_Type;
    FileName  : String := "input.txt";
    begin
        Open(File => InputFile, Mode => In_File, Name => FileName);

        while not End_Of_File loop
             Get(File => InputFile, Item => CurrentFrequency);
             ResultFrequency := ResultFrequency + CurrentFrequency;≤≥
             Pos := Col(File => InputFile);
             Set_Col(File => InputFile, To: Pos + 2);
        end loop;
    end;
    Close(File => InputFile);
    Put(File => Standard_Out, Item => ResultFrequency);
end;