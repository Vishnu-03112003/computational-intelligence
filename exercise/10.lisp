1---Factorial
(defun fact2(n)
    (if (= n 0)1
       (* n (fact2(- n 1)))
    )
)

CL-USER 2 : 1 > (fact2 6)
720

2---Fibonacci
(defun fib2(n)
  (cond
     ((= n 0) 0)
     ((= n 1) 1)
     ((> n 1)(+ (fib2(- n 1))(fib2 (- n 2))))
)
)

CL-USER 4 : 2  (fib2 7)
13

CL-USER 5 : 2 > (fib2 10)
55

3---Palindrome
(defun pali (str)
  (equal str (reverse str)))

CL-USER 15 : 3 > (pali "dhoni")
NIL

CL-USER 16 : 3 > (pali "madam")
T

4---Aree of circle
(defun AreaOfCircle()
  (terpri)
  (princ "Enter Radius:")
  (setq radius (read))
  (setq area (* 3.1416 radius radius))
  (format t "Radius: = ~F~% Area = ~F" radius area)
)

CL-USER 13 : 2 > (AreaOfCircle)

Enter Radius:7
Radius: = 7.0
 Area = 153.9384
