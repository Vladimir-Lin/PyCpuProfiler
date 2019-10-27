var CommonAjaxError = function ( xhr , ajaxOptions , thrownError )
{
  alert ( thrownError + " => " + ajaxOptions ) ;
}

var ReportAjaxProblem = function ( data )
{
  alert ( data [ "Problem" ] ) ;
}

var SilenceAJAX = function ( data )
{
  var tzHtml = data [ "Answer" ] ;
  if ( tzHtml === 'Yes' ) {
  } else {
    ReportAjaxProblem ( data ) ;
  } ;
}

var NormalAJAX = function ( URL , DATA , FUNC , ErrorFunction , asynchronous = false , waiting = "" )
{
  if ( waiting . length > 0 ) {
    $.ajax({
      url: URL ,
      type: "POST" ,
      cache: false ,
      async: asynchronous ,
      dataType: 'json' ,
      data: DATA ,
      success: FUNC ,
      error: function ( ) {
        ErrorFunction ( ) ;
        CloseLoading ( ) ;
      } ,
      beforeSend: function ( ) {
        OpenLoading ( waiting ) ;
      } ,
      complete: function ( XMLHttpRequest , textStatus ) {
        CloseLoading ( ) ;
      }
    });
  } else {
    $.ajax({
      url: URL ,
      type: "POST" ,
      cache: false ,
      async: asynchronous ,
      dataType: 'json' ,
      data: DATA ,
      success: FUNC ,
      error: ErrorFunction ,
    });
  }
}

var AssignAJAX = function ( URL , DATA , asynchronous = false , waiting = "" )
{
  NormalAJAX ( URL , DATA , SilenceAJAX , CommonAjaxError , asynchronous , waiting ) ;
}

var CommonAJAX = function ( URL , DATA , FUNC , asynchronous = false , waiting = "" )
{
  NormalAJAX ( URL , DATA , FUNC , CommonAjaxError , asynchronous , waiting ) ;
}

var FetchByAJAX = function ( URL , DATA , Section , asynchronous = false , waiting = "" )
{
  if ( waiting . length > 0 ) {
    $.ajax({
      url: URL ,
      type: "POST" ,
      cache: false ,
      async: asynchronous ,
      dataType: 'json' ,
      data: DATA ,
      success: function ( data ) {
        var tzHtml = data [ "Answer" ] ;
        if ( tzHtml === "Yes" ) {
          $( Section ) . html ( data [ "Message" ] ) ;
        } else {
        }
      } ,
      beforeSend: function ( ) {
        OpenLoading ( waiting ) ;
      } ,
      complete: function ( XMLHttpRequest , textStatus ) {
        CloseLoading ( ) ;
      }
    });
  } else {
    $.ajax({
      url: URL ,
      type: "POST" ,
      cache: false ,
      async: asynchronous ,
      dataType: 'json' ,
      data: DATA ,
      success: function ( data ) {
        var tzHtml = data [ "Answer" ] ;
        if ( tzHtml === "Yes" ) {
          $( Section ) . html ( data [ "Message" ] ) ;
        } else {
        }
      }
    });
  }
}

var CurrentTimestamp = function ( ) {
  return new Date ( ) . getTime ( ) ;
}

var GetSession = function ( tag )
{
  var answer = { ready: false , value: "" } ;
  CommonAJAX (
    AjaxAssetsPath ( "ajaxGetSession.php" ) ,
    {
      Tag: tag,
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === "Yes" ) {
        answer . ready = true ;
        answer . value = data [ "Value" ] ;
      } else {
      }
    }
  ) ;
  return answer ;
}

var GetSessions = function ( tag , splitter )
{
  var answer = GetSession ( tag ) ;
  var empty  = [ ] ;
  if ( answer . length <= 0 ) return empty ;
  return answer . split ( splitter ) ;
}

var SetSession = function ( tag , value )
{
  var answer = false ;
  CommonAJAX (
    AjaxAssetsPath ( "ajaxSetSession.php" ) ,
    {
      Tag: tag,
      Value: value,
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === "Yes" ) {
        answer = true ;
      } else {
      }
    } ,
    true
  ) ;
  return answer ;
}

var PurgeInput = function ( input )
{
  input = input . replace ( "\t" , "" ) ;
  input = input . replace ( "\r" , "" ) ;
  input = input . replace ( "\n" , "" ) ;
  return  input                         ;
}

var NameChangedWithTable = function ( table , uuid , name , locality , priority = 0 , relevance = 0 )
{
  var v = PurgeInput ( name ) ;
  v = v . trim ( ) ;
  AssignAJAX (
    AjaxAssetsPath ( "ajaxName.php" ) ,
    {
      Table: table ,
      Uuid: uuid ,
      Name: v ,
      Locality: locality ,
      Priority: priority ,
      Relevance: relevance ,
    } ,
    true
  ) ;
}

var DefaultNameChangedNoPurge = function ( uuid , name , locality , priority = 0 , relevance = 0 )
{
  var v = name ;
  v = v . replace ( "\t" , "" ) ;
  v = v . replace ( "\r" , "" ) ;
  v = v . trim    ( ) ;
  AssignAJAX (
    AjaxAssetsPath ( "ajaxName.php" ) ,
    {
      Uuid: uuid,
      Name: v ,
      Locality: locality,
      Priority: priority ,
      Relevance: relevance ,
    } ,
    true
  ) ;
}

var DefaultNameChanged = function ( uuid , name , locality , priority = 0 , relevance = 0 )
{
  var v = PurgeInput ( name ) ;
  v = v . trim ( ) ;
  AssignAJAX (
    AjaxAssetsPath ( "ajaxName.php" ) ,
    {
      Uuid: uuid,
      Name: v ,
      Locality: locality,
      Priority: priority ,
      Relevance: relevance ,
    } ,
    true
  ) ;
}

var ObjectRelation = function ( method , first , second , t1 , t2 , relation , table = "" )
{
  AssignAJAX (
    AjaxAssetsPath ( "ajaxRelation.php" ) ,
    {
      Method: method ,
      First: first ,
      Second: second ,
      T1: t1 ,
      T2: t2 ,
      Relation: relation ,
      Table: table ,
    } ,
    true
  ) ;
}

var GetTranslation = function ( key )
{
  var name = "" ;
  CommonAJAX (
    AjaxAssetsPath ( "ajaxTranslation.php" ) ,
    { Key: key . trim ( ) } ,
    function ( data ) {
      name = data [ "Message" ] ;
    }
  ) ;
  return name ;
}

var GetTranslations = function ( )
{
  var name = { } ;
  CommonAJAX (
    AjaxAssetsPath ( "ajaxTranslations.php" ) ,
    { } ,
    function ( data ) {
      name = data ;
    }
  ) ;
  return name ;
}

var Translations = { } ;

var TranslateIt = function ( key = "" )
{
  if ( ( Translations == undefined ) ||
       ( Translations . length == undefined ) ||
       ( Translations . length <= 0 ) ) {
    Translations = GetTranslations ( ) ;
  }
  if ( key . length <= 0 ) return "" ;
  return Translations [ key ] ;
}

var GetVariable = function ( key )
{
  var name = { } ;
  CommonAJAX (
    AjaxAssetsPath ( "ajaxVariable.php" ) ,
    { Key: key . trim ( ) } ,
    function ( data ) {
      name = data ;
    }
  ) ;
  return name ;
}

var LoadFile = function ( filename )
{
  var file = "";
  CommonAJAX (
    AjaxAssetsPath ( "ajaxFile.php" ) ,
    { Filename: filename } ,
    function ( data ) { file = data [ "Message" ] ; }
  ) ;
  return file ;
}

function FullHeight ( id , topPosition = 20 )
{
  var p = $( id ) . offset ( ) ;
  return parseInt ( $( window ) . height ( ) - p . top - topPosition ) ;
}

var PostURL = function ( url , data , target = "" )
{
  var form                                                            ;
  form   = document . createElement ( "form" )                        ;
  if ( target . length > 0 )                                          {
    form . setAttribute  ( "target" , target )                        ;
  }                                                                   ;
  form   . setAttribute  ( "method" , "post" )                        ;
  form   . setAttribute  ( "action" , url    )                        ;
  for ( key in data )                                                 {
    var hiddenField                                                   ;
    hiddenField = document . createElement ( "input"                ) ;
    hiddenField . setAttribute             ( "type"  , "hidden"     ) ;
    hiddenField . setAttribute             ( "name"  , key          ) ;
    hiddenField . setAttribute             ( "value" , data [ key ] ) ;
    form        . appendChild              ( hiddenField            ) ;
  }
  document . body . appendChild            ( form                   ) ;
  form     . submit                        (                        ) ;
}

var MenuSeparator        = { text: '--' } ;
var ContexturalSeparator = { type: 'seperator' } ;

var QuizletChanged = function ( url , prefer , uuid )
{
  AssignAJAX (
    AjaxAssetsPath ( "ajaxQuizlet.php" ) ,
    {
      Uuid: uuid ,
      Prefer: prefer ,
      URL: PurgeInput ( url ) ,
    } ,
    true
  ) ;
}

var QuizletsChanged = function ( url , prefer , uuid , key , inputclass )
{
  CommonAJAX (
    AjaxAssetsPath ( "ajaxQuizlets.php" ) ,
    {
      Uuid: uuid ,
      Prefer: prefer ,
      URL: PurgeInput ( url ) ,
      Key: key ,
      Input: inputclass ,
    },
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === "Yes" ) {
        $( "#" + key ) . html ( data [ "Message" ] ) ;
      } else {
      }
    } ,
    true
  ) ;
}

var MaterialChanged = function ( url , prefer , uuid )
{
  AssignAJAX (
    AjaxAssetsPath ( "ajaxMaterial.php" ) ,
    {
      Uuid: uuid ,
      Prefer: prefer ,
      URL: PurgeInput ( url ) ,
    } ,
    true
  ) ;
}

var MaterialsChanged = function ( url , prefer , uuid , key , inputclass )
{
  CommonAJAX (
    AjaxAssetsPath ( "ajaxMaterials.php" ) ,
    {
      Uuid: uuid ,
      Prefer: prefer ,
      URL: PurgeInput ( url ) ,
      Key: key ,
      Input: inputclass ,
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === "Yes" ) {
        $( "#" + key ) . html ( data [ "Message" ] ) ;
      } else {
      }
    } ,
    true
  ) ;
}

var FilmPathChanged = function ( url , prefer , uuid )
{
  AssignAJAX (
    AjaxAssetsPath ( "ajaxFilm.php" ) ,
    {
      Uuid: uuid ,
      Prefer: prefer ,
      Film: PurgeInput ( url ) ,
    } ,
    true
  ) ;
}

var FilmUrlChanged = function ( url , prefer , uuid , key , inputclass )
{
  CommonAJAX (
    AjaxAssetsPath ( "ajaxFilms.php" ) ,
    {
      Uuid: uuid ,
      Prefer: prefer ,
      URL: PurgeInput ( url ) ,
      Key: key ,
      Input: inputclass ,
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === "Yes" ) {
        $( "#" + key ) . html ( data [ "Message" ] ) ;
      } else {
      }
    } ,
    true
  ) ;
}

var copyTextToClipboard = function ( text )
{
  var textArea ;
  textArea = document . createElement ( "textarea" ) ;
  textArea . value = text;
  document . body . appendChild ( textArea ) ;
  textArea . select ( ) ;
  document . execCommand ( 'copy' ) ;
  document . body . removeChild ( textArea ) ;
}

var LanguageUsingChanged = function ( language )
{
  CommonAJAX (
    AjaxAssetsPath ( "ajaxSetSession.php" ) ,
    {
      Tag: "CIOS-Language" ,
      Value: language ,
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === "Yes" ) {
        window . location . reload ( ) ;
      }
    } ,
    true
  ) ;
}

var toPeopleString = function ( uuid )
{
  var head = uuid . substr ( 0 , 11 ) ;
  if ( head != "14000000000" ) return "" ;
  return uuid . replace ( "14000000000" , "act1" ) ;
}

var fromPeopleString = function ( puid )
{
  var head = puid . substr ( 0 , 4 ) ;
  if ( head != "act1" ) return "" ;
  return puid . replace ( "act1" , "14000000000" ) ;
}

var toClassString = function ( uuid )
{
  var head = uuid . substr ( 0 , 11 ) ;
  if ( head != "36000000000" ) return "" ;
  return uuid . replace ( "36000000000" , "cls3" ) ;
}

var fromClassString = function ( puid )
{
  var head = puid . substr ( 0 , 4 ) ;
  if ( head != "cls3" ) return "" ;
  return puid . replace ( "cls3" , "36000000000" ) ;
}

var parametersChanged = function ( uuid , type , variety , scope , name , value )
{
  AssignAJAX (
    AjaxAssetsPath ( "ajaxParameters.php" ) ,
    {
      Method: "Data" ,
      Uuid: uuid,
      Type: type,
      Variety: variety,
      Scope: scope,
      Name: name,
      Value: value
    } ,
    true
  ) ;
}

var parameterValueChanged = function ( uuid , type , variety , scope , name , value )
{
  AssignAJAX (
    AjaxAssetsPath ( "ajaxParameters.php" ) ,
    {
      Method: "Value" ,
      Uuid: uuid,
      Type: type,
      Variety: variety,
      Scope: scope,
      Name: name,
      Value: value
    } ,
    true
  ) ;
}

var parameterDateTimeChanged = function ( uuid , type , variety , scope , name , value , tz )
{
  AssignAJAX (
    AjaxAssetsPath ( "ajaxParameters.php" ) ,
    {
      Method: "DateTime" ,
      Uuid: uuid,
      Type: type,
      Variety: variety,
      Scope: scope,
      Name: name,
      Value: value ,
      TZ: tz
    } ,
    true
  ) ;
}

var birthdayChanged = function ( birthday , uuid , key )
{
  if ( birthday . length > 4096 ) return ;
  var dt = birthday . replace ( /-/g , "/" ) ;
  parametersChanged ( uuid , 1 , 14 , "Birthday" , key , dt ) ;
}

var onboardChanged = function ( date , uuid , key )
{
  if ( date . length > 4096 ) return ;
  var dt = date . replace ( /-/g , "/" ) ;
  parametersChanged ( uuid , 1 , 14 , "Onboard" , key , dt ) ;
}

var informationChanged = function ( value , item , uuid )
{
  if ( value . length > 4096 ) return ;
  if ( item  . length > 128  ) return ;
  if ( item  . length < 1    ) return ;
  parametersChanged ( uuid , 1 , 15 , "Information" , item , value ) ;
}

var currencyChanged = function ( value , uuid )
{
  parametersChanged ( uuid , 2 , 43 , "Accounting" , "Currency" , value ) ;
}

var courseChanged = function ( value , uuid )
{
  parametersChanged ( uuid , 2 , 37 , "Teaching" , "Courses" , value ) ;
}

var coursesChanged = function ( lists , key , id , puid )
{
  var kv ;
  var cl = [ ] ;
  lists . forEach ( function ( e ) {
    var checked = $( "#" + id + "-" + e ) . prop ( "checked" ) ;
    if ( checked ) cl . push ( e ) ;
  });
  kv = cl . join ( " , " ) ;
  parametersChanged ( puid , 2 , 37 , "Teaching" , key , kv ) ;
}

var dutyChanged = function ( duty , uuid )
{
  parameterValueChanged ( uuid , 0 , 23 , "Status" , "Duty" , duty ) ;
}

var seniorityChanged = function ( level , uuid )
{
  parameterValueChanged ( uuid , 0 , 23 , "Status" , "Level" , level ) ;
}

var creditChanged = function ( credit , uuid )
{
  parameterValueChanged ( uuid , 0 , 23 , "Status" , "Credit" , credit ) ;
}

var degreeChanged = function ( credit , uuid )
{
  parameterValueChanged ( uuid , 0 , 23 , "Status" , "Degree" , credit ) ;
}

var reposalChanged = function ( credit , uuid )
{
  parameterValueChanged ( uuid , 0 , 23 , "Status" , "Reposal" , credit ) ;
}

var rankChanged = function ( weight , uuid )
{
  parameterValueChanged ( uuid , 1 , 89 , "Priority" , "Weight" , weight ) ;
}

var paymentChanged = function ( payment , uuid )
{
  parameterValueChanged ( uuid , 0 , 48 , "Personal" , "Payment" , payment ) ;
}

var ChangeExpirePeriods = function ( value , uuid )
{
  parameterValueChanged ( uuid , 0 , 37 , "Period" , "Expire" , value ) ;
}

var ChangeRegularPeriods = function ( value , uuid )
{
  parameterValueChanged ( uuid , 0 , 37 , "Period" , "Regular" , value ) ;
}

var offsetChanged = function ( value , uuid )
{
  parameterValueChanged ( uuid , 1 , 14 , "Offset" , "Minutes" , value ) ;
}

var noteItemChanged = function ( method , uuid , prefer , key , note )
{
  AssignAJAX (
    AjaxAssetsPath ( "ajaxNotes.php" ) ,
    {
      Method: method ,
      Uuid: uuid ,
      Prefer: prefer ,
      Key: key ,
      Note: note
    } ,
    true
  ) ;
}

var noteColumnChanged = function ( method , uuid , prefer , key , value )
{
  AssignAJAX (
    AjaxAssetsPath ( "ajaxNotes.php" ) ,
    {
      Method: method ,
      Uuid: uuid ,
      Prefer: prefer ,
      Key: key ,
      Value: value
    } ,
    true
  ) ;
}

var PeopleStatusChanged = function ( value , puid , method )
{
  AssignAJAX(
    AjaxAssetsPath ( "ajaxStates.php" ) ,
    {
      Method: method ,
      Uuid: puid ,
      Value: value ,
    } ,
    true
  ) ;
}

var isPassword = function ( passwd )
{
  if ( passwd . indexOf ( " "  ) >= 0 ) return false ;
  if ( passwd . indexOf ( "'"  ) >= 0 ) return false ;
  if ( passwd . indexOf ( "\"" ) >= 0 ) return false ;
  if ( passwd . indexOf ( "\b" ) >= 0 ) return false ;
  if ( passwd . indexOf ( "\r" ) >= 0 ) return false ;
  if ( passwd . indexOf ( "\n" ) >= 0 ) return false ;
  if ( passwd . indexOf ( "\t" ) >= 0 ) return false ;
  if ( passwd . length           <  8 ) return false ;
  return true ;
}

var AppendBodyHtml = function ( html )
{
  if ( html . length <= 0 ) return ;
  document.body.innerHTML = document.body.innerHTML + html ;
}

var RemoveBodyElement = function ( element )
{
  var el = document . getElementById ( element ) ;
  if ( el ) el . remove ( ) ;
}

var BackToManager = function ( okay , people )
{
  var password = $( "#Password" ) . val ( )    ;
  $( "#BackTo" ) . modal ( "hide" )            ;
  RemoveBodyElement ( "BackTo" )               ;
  if ( ! okay ) return                         ;
  if ( password . length < 8 ) return          ;
  PostURL ( "/login.php"                       ,
            { "actionsid": people              ,
              "actions-password": password } ) ;
}

var BackTo = function ( actid )
{
  RemoveBodyElement ( "BackTo" ) ;
  CommonAJAX (
    AjaxAssetsPath ( "ajaxDialog.php" ) ,
    {
      Method: "Back" ,
      People: actid ,
      ByPass: 1 ,
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === 'Yes' ) {
        $( "body" ) . append ( data [ "Message" ] ) ;
        $( "#BackTo" ) . modal ( "show" ) ;
      } else {
        ReportAjaxProblem ( data ) ;
      } ;
    } ,
    true
  ) ;
}

var SendSmsTo = function ( send )
{
  if ( ! send ) {
    $( "#SmsEditor" ) . modal ( "hide" ) ;
    RemoveBodyElement ( "SmsEditor" ) ;
    return ;
  }

  var number  = $( "#SmsPhoneNumber" ) . val ( ) ;
  var sender  = $( "#SmsSender"      ) . val ( ) ;
  var subject = $( "#SmsSubject"     ) . val ( ) ;
  var content = $( "#SmsContent"     ) . val ( ) ;

  $( "#SmsEditor" ) . modal ( "hide" ) ;
  RemoveBodyElement ( "SmsEditor" ) ;

  CommonAJAX (
    "/commons/portfolio/phones/ajaxMMS.php" ,
    {
      Method: "Send" ,
      Name: sender ,
      Number: number ,
      Subject: subject ,
      Content: content ,
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === 'Yes' ) {
        alert ( data [ "Message" ] ) ;
      } else {
        ReportAjaxProblem ( data ) ;
      } ;
    } ,
    true
  ) ;

}

var SmsDialog = function ( name , target , number )
{
  RemoveBodyElement ( "SmsEditor" ) ;
  CommonAJAX (
    "/commons/portfolio/phones/ajaxMMS.php" ,
    {
      Method: "Dialog" ,
      Name: name ,
      Target: target ,
      Number: number ,
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === 'Yes' ) {
        $( "body" ) . append ( data [ "Message" ] ) ;
        $( "#SmsEditor" ) . modal ( "show" ) ;
      } else {
        ReportAjaxProblem ( data ) ;
      } ;
    } ,
    true
  ) ;
}

var BackendCommand = function ( command , parameters )
{
  var answer = { ready: false , value: "" } ;
  CommonAJAX (
    AjaxAssetsPath ( "ajaxBackend.php" ) ,
    {
      Path: command ,
      Parameters: JSON . stringify ( parameters )
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === "Yes" ) {
        answer . ready = true ;
        answer . value = data ;
      } else {
      }
    } ,
    true
  ) ;
  return answer ;
}

var CloseAlertDialog = function ( )
{
  $( "#AlertDialog" ) . modal ( "hide" ) ;
  RemoveBodyElement ( "AlertDialog" )    ;
}

var AlertDialog = function ( content , title = "" , okay = "" , keycontent = "" , keytitle = "" )
{
  RemoveBodyElement ( "AlertDialog" ) ;
  CommonAJAX (
    AjaxAssetsPath ( "ajaxDialog.php" ) ,
    {
      Method: "Dialog" ,
      Content: content ,
      Title: title ,
      Okay: okay ,
      KeyTitle: keytitle ,
      KeyContent: keycontent ,
      ByPass: 1 ,
    } ,
    function ( data ) {
      var tzHtml = data [ "Answer" ] ;
      if ( tzHtml === 'Yes' ) {
        $( "body" ) . append ( data [ "Message" ] ) ;
        $( "#AlertDialog" ) . modal ( "show" ) ;
      } else {
        ReportAjaxProblem ( data ) ;
      } ;
    } ,
    true
  ) ;
}

var LoadingModalTemplate = "" ;
var LoadingModalPath = "/themes/cheer/top/loading.html" ;

var LoadWaiting = function ( keyword )
{
  if ( LoadingModalTemplate . length <= 0 ) {
    LoadingModalTemplate = LoadFile ( LoadingModalPath ) ;
  }
  var msg = TranslateIt ( keyword ) ;
  modal = LoadingModalTemplate ;
  modal = modal . replace ( "$(LOADING-MESSAGE)" , msg ) ;
  return modal ;
}

var OpenLoading = function ( waiting )
{
  RemoveBodyElement ( "loadingModal" ) ;
  $( "body" ) . append ( waiting ) ;
  $( "#loadingModal" ) . modal ( "show" ) ;
}

var CloseLoading = function ( )
{
  $( "#loadingModal" ) . modal ( "hide" ) ;
  RemoveBodyElement ( "loadingModal" )    ;
  $( "body" ) . removeClass ( "modal-open" ) ;
  $( ".modal-backdrop" ) . remove ( ) ;
}
