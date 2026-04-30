% --- Helper Predicate: Member ---
% Checks if an element X exists in a list.
my_member(X, [X|_]).
my_member(X, [_|T]) :- my_member(X, T).

% --- 1. Cardinality ---
% The number of elements in the set.
cardinality([], 0).
cardinality([_|T], N) :-
    cardinality(T, N1),
    N is N1 + 1.

% --- 2. Subset ---
% Subset(A, B) is true if every element of A is in B.
subset([], _).
subset([H|T], SetB) :-
    my_member(H, SetB),
    subset(T, SetB).

% --- 3. Equivalence (Equality) ---
% Two sets are equivalent if A is a subset of B AND B is a subset of A.
equivalence(SetA, SetB) :-
    subset(SetA, SetB),
    subset(SetB, SetA).

% --- 4. Union ---
% Combines elements from both sets, removing duplicates.
union([], Set2, Set2).
union([H|T], Set2, Result) :-
    my_member(H, Set2), !, % If H is already in Set2, skip it to avoid duplicates
    union(T, Set2, Result).
union([H|T], Set2, [H|Result]) :-
    union(T, Set2, Result).

% --- 5. Intersection ---
% Elements that are present in both sets.
intersection([], _, []).
intersection([H|T], Set2, [H|Result]) :-
    my_member(H, Set2), !,
    intersection(T, Set2, Result).
intersection([_|T], Set2, Result) :-
    intersection(T, Set2, Result).

% --- 6. Difference (SetA - SetB) ---
% Elements in SetA that are NOT in SetB.
difference([], _, []).
difference([H|T], SetB, Result) :-
    my_member(H, SetB), !,
    difference(T, SetB, Result).
difference([H|T], SetB, [H|Result]) :-
    difference(T, SetB, Result).




test case:
% c:/Users/Administrator/Documents/Prolog/set.pl compiled 0.00 sec, 16 clauses
?- cardinality([a, b, c], X).
X = 3.

?- subset([1, 2], [1, 2, 3]).
true .

?- subset([1, 4], [1, 2, 3]).
false.

?- equivalence([a, b], [b, a]).
true .

?- equivalence([a, b], [a, c]).
false.

?- union([1, 2, 3], [3, 4, 5], X).
X = [1, 2, 3, 4, 5].

?- intersection([1, 2, 3], [2, 3, 4], X).
X = [2, 3].

?- intersection([1, 2], [3, 4], X).
X = [].

?- difference([1, 2, 3], [2], X).
X = [1, 3].

?- difference([a, b], [c, d], X).
X = [a, b].

?- cardinality([], X).
X = 0.

?- subset([], [1, 2]).
true.

?- union([], [1, 2], X).
X = [1, 2].

?- intersection([1, 2], [], X).
X = [].
[23bcs033@mepcolinux ex6a]$cat calculator.txt
% Main entry point to start the calculator
calculator :-
    nl,
    write('--- MENU DRIVEN CALCULATOR ---'), nl,
    write('1. Addition'), nl,
    write('2. Subtraction'), nl,
    write('3. Multiplication'), nl,
    write('4. Division'), nl,
    write('5. Modulus'), nl,
    write('6. Exit'), nl,
    write('Enter your choice: '),
    read(Choice),
    process(Choice).

% Process 1: Addition
process(1) :-
    write('Enter Number 1: '), read(N1),
    write('Enter Number 2: '), read(N2),
    Res is N1 + N2,
    format('Sum: ~w + ~w = ~w~n', [N1, N2, Res]),
    calculator. % Loop back to menu

% Process 2: Subtraction
process(2) :-
    write('Enter Number 1: '), read(N1),
    write('Enter Number 2: '), read(N2),
    Res is N1 - N2,
    format('Difference: ~w - ~w = ~w~n', [N1, N2, Res]),
    calculator.

% Process 3: Multiplication
process(3) :-
    write('Enter Number 1: '), read(N1),
    write('Enter Number 2: '), read(N2),
    Res is N1 * N2,
    format('Product: ~w * ~w = ~w~n', [N1, N2, Res]),
    calculator.

% Process 4: Division
process(4) :-
    write('Enter Number 1: '), read(N1),
    write('Enter Number 2: '), read(N2),
    (N2 =:= 0 ->
        write('Error: Cannot divide by zero!'), nl
    ;
        Res is N1 / N2,
        format('Division: ~w / ~w = ~w~n', [N1, N2, Res])
    ),
    calculator.

% Process 5: Modulus
process(5) :-
    write('Enter Number 1: '), read(N1),
    write('Enter Number 2: '), read(N2),
    (N2 =:= 0 ->
        write('Error: Cannot perform mod by zero!'), nl
    ;
        Res is N1 mod N2,
        format('Remainder: ~w mod ~w = ~w~n', [N1, N2, Res])
    ),
    calculator.

% Process 6: Exit
process(6) :-
    write('Exiting... Goodbye!'), nl, !.

% Process for Invalid Inputs
process(_) :-
    write('Invalid Choice! Please select 1-6.'), nl,
    calculator.
