cl_fine = 0.01;
cl_finer = 0.005;

// Outer points
Point(1) = {-0.65, -0.65, 0, cl_fine};
Point(2) = {0.65, -0.65, 0, cl_fine};
Point(3) = {-0.65, 0.65, 0, cl_fine};
Point(4) = {0.65, 0.65, 0, cl_fine};

// Geometry features
// Black
Point(5) = {-0.65, 0.6, 0, cl_fine};
Point(6) = {0.65, 0.6, 0, cl_fine};
Point(7) = {-0.65, -0.6, 0, cl_fine};
Point(8) = {0.65, -0.6, 0, cl_fine};

// Red
Point(9) = {-0.65, 0.4, 0, cl_fine};
Point(10) = {-0.6, 0.4, 0, cl_fine};
Point(11) = {-0.6, -0.4, 0, cl_fine};
Point(12) = {-0.65, -0.4, 0, cl_fine};

Point(13) = {0.65, 0.4, 0, cl_fine};
Point(14) = {0.6, 0.4, 0, cl_fine};
Point(15) = {0.6, -0.4, 0, cl_fine};
Point(16) = {0.65, -0.4, 0, cl_fine};

// Green (and blue)
Point(17) = {-0.2, -0.4, 0, cl_finer};
Point(18) = {-0.2, 0.4, 0, cl_finer};
Point(19) = {0.2, 0.4, 0, cl_finer};
Point(20) = {0.2, -0.4, 0, cl_finer};

Point(21) = {-0.15, -0.35, 0, cl_finer};
Point(22) = {-0.15, 0.35, 0, cl_finer};
Point(23) = {0.15, 0.35, 0, cl_finer};
Point(24) = {0.15, -0.35, 0, cl_finer};


// Helper points and lines
Point(25) = {-0.6, 0.6, 0, cl_fine};
Point(26) = {-0.6, -0.6, 0, cl_fine};
Point(27) = {0.6, 0.6, 0, cl_fine};
Point(28) = {0.6, -0.6, 0, cl_fine};

Point(37) = {-0.6, 0.65, 0, cl_fine};
Point(38) = {-0.6, -0.65, 0, cl_fine};
Point(39) = {0.6, 0.65, 0, cl_fine};
Point(40) = {0.6, -0.65, 0, cl_fine};


Point(56) = { cl_fine, -0.6 , 0, cl_finer*2};
Point(41) = { - cl_fine, -0.6, 0, cl_finer*2};
Point(42) = {cl_fine, -0.6 + cl_fine, 0, cl_finer*2};
Point(43) = {-cl_fine, -0.6 + cl_fine, 0, cl_finer*2};

Point(44) = { cl_fine, 0.6 , 0, cl_finer*2};
Point(45) =  { - cl_fine, 0.6 , 0, cl_finer*2};
Point(46) = {cl_fine, 0.6 - cl_fine, 0, cl_finer*2};
Point(47) = {-cl_fine, 0.6 - cl_fine, 0, cl_finer*2};

Point(48) = {-0.4 + cl_fine,  cl_fine, 0, cl_finer*2};
Point(49) = {-0.4 - cl_fine,  cl_fine, 0, cl_finer*2};
Point(50) = {-0.4 + cl_fine,  -cl_fine, 0, cl_finer*2};
Point(51) = {-0.4 - cl_fine,  -cl_fine, 0, cl_finer*2};

Point(52) = {0.4 + cl_fine,  cl_fine, 0, cl_finer*2};
Point(53) = {0.4 - cl_fine,  cl_fine, 0, cl_finer*2};
Point(54) = {0.4 + cl_fine,  -cl_fine, 0, cl_finer*2};
Point(55) = {0.4 - cl_fine,  -cl_fine, 0, cl_finer*2};

// Lines of basic geometric features
//+
Line(1) = {3, 5};
//+
//+
Line(3) = {6, 4};
//+
Line(5) = {7, 1};
//+
Line(8) = {2, 8};
//+
//+
Line(10) = {12, 11};
//+
//+
Line(13) = {10, 9};
//+
//+
Line(15) = {15, 16};
//+
//+
Line(17) = {13, 14};
//+
//+
Line(19) = {21, 24};
//+
Line(20) = {24, 23};
//+
Line(21) = {23, 22};
//+
Line(22) = {22, 21};
//+
//Line(26) = {19, 18};
//+
Line(28) = {5, 9};
//+
Line(29) = {12, 7};
//+q
Line(30) = {8, 16};
//+
Line(31) = {13, 6};

//+
Line(32) = {1, 38};
//+
Line(33) = {38, 40};
//+
Line(34) = {40, 2};
//+
Line(36) = {7, 26};
//+
Line(37) = {26, 11};
//+
Line(38) = {11, 10};
//+
Line(39) = {9, 12};
//+
Line(40) = {10, 25};
//+
Line(41) = {25, 37};
//+
Line(42) = {37, 3};
//+
Line(43) = {5, 25};
//+
Line(45) = {27, 6};
//+
Line(46) = {4, 39};
//+
Line(47) = {39, 37};
//+
Line(48) = {14, 27};
//+
Line(49) = {27, 39};
//+
Line(50) = {13, 16};
//+
Line(51) = {15, 14};
//+
Line(52) = {28, 15};
//+
Line(53) = {28, 8};
//+
Line(54) = {28, 40};
//+
Line(55) = {26, 38};
//+
Line(56) = {17, 18};
//+
Line(57) = {18, 19};
//+
Line(58) = {19, 20};
//+
Line(59) = {20, 17};
//+
Curve Loop(1) = {38, 13, 39, 10};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {37, -10, 29, 36};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {55, -32, -5, 36};
//+
Plane Surface(3) = {3};
//+
//+
Curve Loop(5) = {34, 8, -53, 54};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {52, 15, -30, -53};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {51, -17, 50, -15};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {17, 48, 45, -31};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {45, 3, 46, -49};
//+
Plane Surface(9) = {9};
//+

//+
Curve Loop(11) = {43, 41, 42, 1};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {40, -43, 28, -13};
//+
Plane Surface(12) = {12};
//+

//+

//+
Curve Loop(15) = {20, 21, 22, 19};
//+
Plane Surface(15) = {15};
//+
//+
Physical Curve("inflow", 60) = {28, 29, 30, 31};
//+
Physical Curve("void", 60) += {1, 42, 47, 46, 3, 50, 8, 34, 33, 32, 5, 39};
//+
Line(60) = {26, 41};
//+
Line(61) = {41, 56};
//+
Line(62) = {56, 28};
//+
Line(63) = {41, 43};
//+
Line(64) = {43, 42};
//+
Line(65) = {42, 56};
//+
Line(66) = {49, 51};
//+
Line(67) = {51, 50};
//+
Line(68) = {50, 48};
//+
Line(69) = {48, 49};
//+
Line(70) = {53, 55};
//+
Line(71) = {55, 54};
//+
Line(72) = {54, 52};
//+
Line(73) = {52, 53};
//+
Line(74) = {25, 45};
//+
Line(75) = {45, 44};
//+
Line(76) = {44, 27};
//+
Line(77) = {45, 47};
//+
Line(78) = {47, 46};
//+
Line(79) = {46, 44};
//+
Curve Loop(16) = {55, 33, -54, -62, -61, -60};
//+
Plane Surface(16) = {16};
//+
Curve Loop(17) = {61, -65, -64, -63};
//+
Plane Surface(17) = {17};
//+
Curve Loop(18) = {71, 72, 73, 70};
//+
Plane Surface(18) = {18};
//+
Curve Loop(19) = {67, 68, 69, 66};
//+
Plane Surface(19) = {19};
//+
Curve Loop(20) = {76, 49, 47, -41, 74, 75};
//+
Plane Surface(20) = {20};
//+
Curve Loop(21) = {77, 78, 79, -75};
//+
Plane Surface(21) = {21};
//+
Curve Loop(22) = {74, 77, 78, 79, 76, -48, -51, -52, -62, -65, -64, -63, -60, 37, 38, 40};
//+
Curve Loop(23) = {58, 59, 56, 57};
//+
Plane Surface(22) = {18, 19, 22, 23};
//+
Plane Surface(23) = {15, 23};

Recombine Surface "*";
