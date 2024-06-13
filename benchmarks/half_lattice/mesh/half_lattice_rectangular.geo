cl_fine = 0.01;
cl_mid = cl_fine * 2;
cl_coarse = cl_fine * 4;
cl_coarsest = cl_fine * 6;

Point(2) = {3.5, -3.5, 0, cl_coarsest};

Point(4) = {3.5, 3.5, 0, cl_coarsest};
Point(131) = { 0.0, -3.5, 0, cl_coarsest };
Point(142) = { 0.0, 3.5, 0, cl_coarsest };


Recombine Surface "*";
//+
Line(1) = {142, 4};
//+
Line(2) = {2, 4};
//+
Line(3) = {2, 131};
//+
Line(4) = {131, 142};
//+
Curve Loop(1) = {4, 1, -2, 3};
//+
Plane Surface(1) = {1};
Transfinite Surface {1};
Physical Curve("void", 61) =  {1, 2, 3};
Physical Curve("reflecting", 4);
Recombine Surface "*";