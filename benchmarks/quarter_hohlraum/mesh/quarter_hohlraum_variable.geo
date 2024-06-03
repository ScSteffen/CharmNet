cl_fine = 0.005;
cl_coarse =cl_fine*2;
upper_right_red = 0.4;
horizontal_right_red = 0.6;

// Outer points
Point(1) = {0.65, 0.65, 0, cl_coarse};
Point(2) = {0., 0.65, 0, cl_coarse};
Point(3) = {0.65, 0., 0, cl_coarse};
Point(4) = {0., 0., 0, cl_coarse};

// Geometry features
// Black
Point(6) = {0.65, 0.6, 0, cl_coarse};

Point(13) = {0.65,upper_right_red, 0, cl_coarse*1.5};
Point(14) = {horizontal_right_red, upper_right_red, 0, cl_fine};
Point(15) = {horizontal_right_red, 0.0, 0, cl_fine};


// Green (and blue)

Point(19) = {0.2, 0.4, 0, cl_fine};
Point(20) = {0, 0.4, 0, cl_fine};
Point(21) = {0.2, 0, 0, cl_fine};

Point(22) = {0.15, 0.35, 0, cl_fine};
Point(23) = {0.0, 0.35, 0, cl_fine};
Point(24) = {0.15, 0.0, 0, cl_fine};



// Helper points and lines
Point(27) = {horizontal_right_red, 0.6, 0, cl_coarse};
Point(28) = {0.4, 0.0, 0, cl_coarse};



Point(45) =  { 0, 0.6 , 0, cl_fine*2};

//+
Line(1) = {2, 1};
//+
Line(2) = {1, 6};
//+
Line(3) = {6, 13};
//+
Line(4) = {13, 3};
//+
Line(5) = {3, 15};

//+
Line(7) = {28, 21};
Line(13) = {15, 28};
//+
Line(8) = {21, 24};
//+
Line(9) = {24, 4};
//+
Line(10) = {4, 23};
//+
Line(11) = {23, 20};
//+
Line(12) = {20, 45};
//+
//+
Line(14) = {45, 2};


Line(15) = {24, 22};
//+
Line(16) = {22, 23};
//+
Line(17) = {20, 19};
//+
Line(18) = {19, 21};
//+
Line(24) = {45, 27};
//+
Line(26) = {27, 6};
//+
Line(27) = {27, 14};
//+
Line(28) = {14, 13};
//+
//+
Line(30) = {14, 15};
//+
Curve Loop(1) = {10, -16, -15, 9};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {18, 8, 15, 16, 11, 17};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {7,13, -18, -17, 12, 24, 27, 30};
//+
Plane Surface(3) = {3};
//+
Curve Loop(6) = {5, -30, 28, 4};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {28, -3, -26, 27};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {24, 26, -2, -1, -14};
//+
Plane Surface(8) = {8};


Physical Curve("inflow", 60) = {3};
//+
Physical Curve("void", 61) = {1, 2,  4, 5, 6, 7, 8, 9, 10, 11, 12,13,14, 29};