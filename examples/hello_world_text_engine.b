character table for all lower case characters in the alphabet

// ASCII lookup table
a: 97; b: 98; c: 99; d:100; e:101;
f:102; g:103; h:104; i:105; j:106;
k:107; l:108; m:109; n:110; o:111;
p:112; q:113; r:114; s:115; t:116;
u:117; v:118; w:119; x:120; y:121;
z:122;
 
// initialize char table
+++++ +++++
[
 > +++++ +++++
 < -
]                   #0: 0; #1: 100
> ---               #1: 97;

// initialize counter
1 >>> 4 +++++
[
 < +++++
 > -
]                   #3: 25;
4 <<< 1

// create char table
1 >> 3
[
 3 << 1
 [
  1 < 0 +
  0 >> 2 +
  2 < 1 -
 ]                   #0: 97; #1:  0; #2: 97; #3: 97;
 > + <               increment
 1 >> 3
 [>+<-]              move counter one right
 > -                 set pointer to counter and decrement
]
28 << [<+>-]< 25

// add space to char table
>> +++++
[
 < +++++ +
 > -
]
< ++                 #26: 32 = space

// add period to char table
>> +++++ +++
[
 < +++++ +
 > -
] < --               #27: 46 = period

// move pointer to 0

27 <<<<< <<<<< <<<<< <<<<< <<<<< << 0

// write text : abcdefghijklmnopqrstuvwxyz{space}{period}
>>>>>>> h. <<< e. >>>>>>> l. l. >>> o.
>>>>>>>>>>>> space.
<<<< w. <<<<<<<< o. >>> r. <<<<<< l. <<<<<<<< d.
>>>>>>>>>>>>>>>>>>>>>>>> period.