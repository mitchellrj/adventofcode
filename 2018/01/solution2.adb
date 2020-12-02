with Ada.Containers.Vectors;
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;


procedure OneTwo is
    package Seen_Vecs is new Ada.Containers.Vectors(Element_Type => Integer, Index_Type => Natural);
    use Seen_Vecs;
    Position         : Seen_Vecs.Cursor;
    SeenFrequencies  : Seen_Vecs.Vector;
    ResultFrequency  : Integer := 0;
    CurrentFrequency : Integer := 0;
    InputFile        : File_Type;
    FileName         : String := "input.txt";
    Found            : Boolean := False;
begin
    loop
        Seen_Vecs.Append(SeenFrequencies, 0);
        begin
            Open(File => InputFile, Mode => In_File, Name => FileName);

            loop
                Get(File => InputFile, Item => CurrentFrequency);
                ResultFrequency := ResultFrequency + CurrentFrequency;
                Position := Seen_Vecs.First(SeenFrequencies);
                if Seen_Vecs.Contains(SeenFrequencies, ResultFrequency) then
                        Put(ResultFrequency);
                        Found := True;
                        exit;
                    end if;
                exit when End_Of_File(File => InputFile);
            Seen_Vecs.Append(SeenFrequencies, ResultFrequency);
            Skip_Line(File => InputFile);
            end loop;
        end;
        Close(File => InputFile);
    exit when Found;
    end loop;
end OneTwo;