cl_fine = 0.05;
upper_right_red = 0.4;
horizontal_right_red = 0.6;


// Outer points
Point(1) = {0.65, 0.65, 0, cl_fine};
Point(2) = {0., 0.65, 0, cl_fine};
Point(3) = {0.65, 0., 0, cl_fine};
Point(4) = {0., 0., 0, cl_fine};
//+
Line(1) = {2, 1};
//+
Line(2) = {1, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 2};
//+
Curve Loop(1) = {4, 1, 2, 3};
//+
Plane Surface(1) = {1};
//+
Transfinite Surface {1};

Physical Curve("inflow", 60) = {2};
//+
Physical Curve("void", 61) =  {1, 3, 4};
Recombine Surface "*";