
cl_fine = 0.01;

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
Point(17) = {-0.2, -0.4, 0, cl_fine};
Point(18) = {-0.2, 0.4, 0, cl_fine};
Point(19) = {0.2, 0.4, 0, cl_fine};
Point(20) = {0.2, -0.4, 0, cl_fine};

Point(21) = {-0.15, -0.35, 0, cl_fine};
Point(22) = {-0.15, 0.35, 0, cl_fine};
Point(23) = {0.15, 0.35, 0, cl_fine};
Point(24) = {0.15, -0.35, 0, cl_fine};




// Lines of basic geometric features
//+
Line(1) = {3, 5};
//+
//+
Line(3) = {6, 4};
//+
//+
Line(5) = {7, 1};
//+
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
//+
Line(30) = {8, 16};
//+
Line(31) = {13, 6};

// Helper points and lines
Point(25) = {-0.6, 0.6, 0, cl_fine};
Point(26) = {-0.6, -0.6, 0, cl_fine};
Point(27) = {0.6, 0.6, 0, cl_fine};
Point(28) = {0.6, -0.6, 0, cl_fine};
//+
Line(32) = {25, 10};
//+
Line(33) = {11, 26};
//+
Line(34) = {27, 14};
//+
Line(35) = {15, 28};

Point(29) = {-0.15, -0.4, 0, cl_fine};
Point(30) = {0.15, -0.4, 0, cl_fine};
Point(31) = {0.15, 0.4, 0, cl_fine};
Point(32) = {-0.15, 0.4, 0, cl_fine};


Point(33) = {0.2, -0.6, 0, cl_fine};
Point(34) = {-0.2, -0.6, 0, cl_fine};
Point(35) = {-0.2, 0.6, 0, cl_fine};
Point(36) = {0.2, 0.6, 0, cl_fine};
//+
Line(47) = {25, 35};
//+

//+
Line(49) = {36, 27};
//+
Line(50) = {26, 34};
//+

//+
Line(52) = {33, 28};
//+
Line(53) = {7, 26};
//+
Line(54) = {28, 8};
//+
Point(37) = {0.2, -0.35, 0, cl_fine};
Point(38) = {-0.2, -0.35, 0, cl_fine};
Point(39) = {-0.2, 0.35, 0, cl_fine};
Point(40) = {0.2,  0.35, 0, cl_fine};
//+
Line(55) = {18, 39};
//+
Line(56) = {39, 38};
//+
Line(57) = {38, 17};
//+
Line(58) = {20, 37};
//+
Line(59) = {37, 40};
//+
Line(60) = {40, 19};
//+
Line(61) = {40, 23};
//+
Line(62) = {23, 31};
//+
Line(63) = {22, 32};
//+
Line(64) = {22, 39};
//+
Line(65) = {38, 21};
//+
Line(66) = {21, 29};
//+
Line(67) = {24, 30};
//+
Line(68) = {24, 37};
//+
Line(69) = {27, 6};
//+
Line(70) = {25, 5};

Point(41) = {-0.6,  0.35, 0, cl_fine};
Point(42) = {0.6,  -0.35, 0, cl_fine};
Point(43) = {0.6,  0.35, 0, cl_fine};
Point(44) = {-0.6,  -0.35, 0, cl_fine};

Point(45) = {-0.65,  0.35, 0, cl_fine};
Point(46) = {0.65,  -0.35, 0, cl_fine};
Point(47) = {0.65,  0.35, 0, cl_fine};
Point(48) = {-0.65,  -0.35, 0, cl_fine};

Point(49) = {0.15,  -0.6, 0, cl_fine};
Point(50) = {-0.15,  0.6, 0, cl_fine};
Point(51) = {-0.15,  -0.6, 0, cl_fine};
Point(52) = {0.15,  0.6, 0, cl_fine};


Point(53) = {-0.6, -0.65, 0, cl_fine};
Point(54) = {0.6, -0.65, 0, cl_fine};
Point(55) = {0.6, 0.65, 0, cl_fine};
Point(56) = {-0.6, 0.65, 0, cl_fine};

Point(57) = {-0.2, -0.65, 0, cl_fine};
Point(58) = {0.2, -0.65, 0, cl_fine};
Point(59) = {0.2, 0.65, 0, cl_fine};
Point(60) = {-0.2, 0.65, 0, cl_fine};

Point(61) = {-0.15, -0.65, 0, cl_fine};
Point(62) = {0.15, -0.65, 0, cl_fine};
Point(63) = {0.15, 0.65, 0, cl_fine};
Point(64) = {-0.15, 0.65, 0, cl_fine};
//+
//+
Line(71) = {9, 45};
//+
Line(72) = {45, 41};
//+
Line(73) = {41, 10};
//+
Line(74) = {11, 44};
//+
Line(75) = {44, 48};
//+
Line(76) = {48, 12};
//+
Line(77) = {45, 48};
//+
Line(78) = {44, 41};
//+
Line(79) = {14, 43};
//+
Line(80) = {43, 47};
//+
Line(81) = {47, 13};
//+
Line(82) = {42, 15};
//+
Line(83) = {46, 16};
//+
Line(84) = {42, 46};
//+
Line(85) = {46, 47};
//+
Line(86) = {43, 42};
//+
Line(87) = {35, 18};
//+
Line(88) = {32, 50};
//+
Line(89) = {35, 50};
//+
Line(90) = {50, 52};
//+
Line(91) = {52, 31};
//+
Line(92) = {19, 36};
//+
Line(93) = {36, 52};
//+
Line(94) = {34, 51};
//+
Line(95) = {51, 29};
//+
Line(96) = {17, 34};
//+
Line(97) = {30, 49};
//+
Line(98) = {33, 20};
//+
Line(99) = {33, 49};
//+
Line(100) = {49, 51};
//+
Line(101) = {20, 15};
//+
Line(102) = {37, 42};
//+
Line(103) = {40, 43};
//+
Line(104) = {19, 14};
//+
Line(105) = {10, 18};
//+
Line(106) = {41, 39};
//+
Line(107) = {44, 38};
//+
Line(108) = {11, 17};
//+
Line(109) = {17, 29};
//+
Line(110) = {29, 30};
//+
Line(111) = {30, 20};
//+
Line(112) = {18, 32};
//+
Line(113) = {32, 31};
//+
Line(114) = {31, 19};
//+
Curve Loop(1) = {22, 19, 20, 21};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {65, -22, 64, 56};
//+
Plane Surface(2) = {2};//+
Curve Loop(3) = {63, -112, 55, -64};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {61, 62, 114, -60};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {21, 63, 113, -62};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {20, -61, -59, -68};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {68, -58, -111, -67};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {110, -67, -19, 66};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {109, -66, -65, 57};
//+
Plane Surface(9) = {9};
//+
//+
Curve Loop(10) = {56, -107, 78, 106};
//+
Plane Surface(10) = {10};
//+
Curve Loop(11) = {102, -86, -103, -59};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {104, 79, -103, 60};
//+
Plane Surface(12) = {12};
//+
Curve Loop(13) = {104, -34, -49, -92};
//+
Plane Surface(13) = {13};
//+
Curve Loop(14) = {17, -34, 69, -31};
//+
Plane Surface(14) = {14};
//+
Curve Loop(15) = {80, 81, 17, 79};
//+
Plane Surface(15) = {15};
//+
Curve Loop(16) = {86, 84, 85, -80};
//+
Plane Surface(16) = {16};
//+
Curve Loop(17) = {84, 83, -15, -82};
//+
Plane Surface(17) = {17};
//+
Curve Loop(18) = {35, 54, 30, -15};
//+
Plane Surface(18) = {18};
//+
Curve Loop(19) = {101, -82, -102, -58};
//+
Plane Surface(19) = {19};
//+
Curve Loop(20) = {98, 101, 35, -52};
//+
Plane Surface(20) = {20};
//+
Curve Loop(21) = {98, -111, 97, -99};
//+
Plane Surface(21) = {21};
//+
Curve Loop(22) = {110, 97, 100, 95};
//+
Plane Surface(22) = {22};
//+
Curve Loop(23) = {109, -95, -94, -96};
//+
Plane Surface(23) = {23};
//+
Curve Loop(24) = {112, 88, -89, 87};
//+
Plane Surface(24) = {24};
//+
Curve Loop(25) = {113, -91, -90, -88};
//+
Plane Surface(25) = {25};
//+
Curve Loop(26) = {114, 92, 93, 91};
//+
Plane Surface(26) = {26};
//+
Curve Loop(27) = {105, -87, -47, 32};
//+
Plane Surface(27) = {27};
//+
Curve Loop(28) = {13, -28, -70, 32};
//+
Plane Surface(28) = {28};
//+
Curve Loop(29) = {72, 73, 13, 71};
//+
Plane Surface(29) = {29};
//+
Curve Loop(30) = {78, -72, 77, -75};
//+
Plane Surface(30) = {30};
//+
Curve Loop(31) = {74, 75, 76, 10};
//+
Plane Surface(31) = {31};
//+
Curve Loop(32) = {33, -53, -29, 10};
//+
Plane Surface(32) = {32};
//+
Curve Loop(33) = {50, -96, -108, 33};
//+
Plane Surface(33) = {33};
//+
Curve Loop(34) = {108, -57, -107, -74};
//+
Plane Surface(34) = {34};
//+

//+
Curve Loop(37) = {106, -55, -105, -73};
//+
Plane Surface(37) = {37};


//+
Transfinite Surface {2};
//+
Transfinite Surface {1};
//+
Transfinite Surface {6};
//+
Transfinite Surface {5};
//+
Transfinite Surface {4};
//+
Transfinite Surface {3};
//+
Transfinite Surface {9};
//+
Transfinite Surface {8};
//+
//+
Transfinite Surface {10};
//+
Transfinite Surface {37};
//+
Transfinite Surface {27};
//+
Transfinite Surface {24};
//+
Transfinite Surface {25};
//+
Transfinite Surface {13};
//+
Transfinite Surface {26};
//+
Transfinite Surface {12};
//+
Transfinite Surface {11};
//+
Transfinite Surface {19};
//+
Transfinite Surface {20};
//+
Transfinite Surface {35};
//+
Transfinite Surface {21};
//+
Transfinite Surface {22};
//+
Transfinite Surface {23};
//+
Transfinite Surface {33};
//+
Transfinite Surface {32};
//+
Transfinite Surface {31};
//+
Transfinite Surface {30};
//+
//+
Transfinite Surface {18};
//+
Transfinite Surface {17};
//+
Transfinite Surface {16};
//+
Transfinite Surface {12};
//+
Transfinite Surface {15};
//+
Transfinite Surface {14};
//+
//+
Transfinite Surface {26};
//+
Transfinite Surface {24};
//+
Transfinite Surface {28};
//+
Transfinite Surface {29};
//+
Transfinite Surface {30};
//+
Transfinite Surface {23};
//



//+
Line(115) = {1, 53};
//+
Line(116) = {53, 26};
//+
Line(117) = {53, 57};
//+
Line(118) = {57, 34};
//+
Line(119) = {57, 61};
//+
Line(120) = {61, 51};
//+
Line(121) = {61, 62};
//+
Line(122) = {62, 49};
//+
Line(123) = {62, 58};
//+
Line(124) = {58, 33};
//+
Line(125) = {58, 54};
//+
Line(126) = {54, 28};
//+
Line(128) = {54, 2};
//+
Line(129) = {4, 55};
//+
Line(130) = {55, 27};
//+
Line(131) = {55, 59};
//+
Line(132) = {59, 36};
//+
Line(133) = {59, 63};
//+
Line(134) = {63, 52};
//+
Line(135) = {63, 64};
//+
Line(136) = {64, 50};
//+
Line(137) = {64, 60};
//+
Line(138) = {60, 35};
//+
Line(139) = {60, 56};
//+
Line(140) = {56, 25};
//+
Line(141) = {56, 3};
//+
Curve Loop(38) = {140, 70, -1, -141};
//+
Plane Surface(38) = {38};
//+
Curve Loop(39) = {139, 140, 47, -138};
//+
Plane Surface(39) = {39};
//+
Curve Loop(40) = {137, 138, 89, -136};
//+
Plane Surface(40) = {40};
//+
Curve Loop(41) = {135, 136, 90, -134};
//+
Plane Surface(41) = {41};
//+
Curve Loop(42) = {133, 134, -93, -132};
//+
Plane Surface(42) = {42};
//+
Curve Loop(43) = {49, -130, 131, 132};
//+
Plane Surface(43) = {43};
//+
Curve Loop(44) = {69, 3, 129, 130};
//+
Plane Surface(44) = {44};
//+
Curve Loop(45) = {128, 8, -54, -126};
//+
Plane Surface(45) = {45};
//+
Curve Loop(46) = {125, 126, -52, -124};
//+
Plane Surface(46) = {46};
//+
Curve Loop(47) = {123, 124, 99, -122};
//+
Plane Surface(47) = {47};
//+
Curve Loop(48) = {121, 122, 100, -120};
//+
Plane Surface(48) = {48};
//+
Curve Loop(49) = {119, 120, -94, -118};
//+
Plane Surface(49) = {49};
//+
Curve Loop(50) = {117, 118, -50, -116};
//+
Plane Surface(50) = {50};
//+
Curve Loop(51) = {115, 116, -53, 5};
//+
Plane Surface(51) = {51};


Transfinite Surface {51};
//+
Transfinite Surface {50};
//+
Transfinite Surface {49};
//+
Transfinite Surface {48};
//+
Transfinite Surface {47};
//+
Transfinite Surface {46};
//+
Transfinite Surface {45};
//+
Transfinite Surface {44};
//+
Transfinite Surface {43};
//+
Transfinite Surface {42};
//+
Transfinite Surface {41};
//+
Transfinite Surface {40};
//+
Transfinite Surface {39};
//+
Transfinite Surface {38};
//+
Transfinite Surface {7};
Transfinite Surface {34};

Physical Curve("void", 142) = {28, 71, 77, 76, 29, 5, 115, 117, 119, 121, 123, 125, 128, 8, 30, 83, 85, 81, 31, 3, 129, 131, 133, 135, 137, 139, 141, 1};

Recombine Surface "*";
//+
//+
