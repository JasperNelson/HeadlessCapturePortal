function facebookLogin() {

    executePost3(getAppUrl() + 'signin/facebook', 'acceptTerms', getAcceptTermsVal());
}

function instagramLogin() {

    executePost3(getAppUrl() + 'signin/instagram', 'acceptTerms', getAcceptTermsVal());
}


function facebookWifiLogin() {

    executePost3(getAppUrl() + 'signin/facebookwifi', 'acceptTerms', getAcceptTermsVal());
}

function googleLogin() {
    executePost3(getAppUrl() + 'signin/google', 'acceptTerms', getAcceptTermsVal());
}

function adfsLogin() {
    executePost3(getAppUrl() + 'signin/adfs', 'acceptTerms', getAcceptTermsVal());
}

function twitterLogin() {
    executePost3(getAppUrl() + 'signin/twitter', 'acceptTerms', getAcceptTermsVal());
}

function linkedinLogin() {
    executePost3(getAppUrl() + 'signin/linkedin2', 'acceptTerms', getAcceptTermsVal());
}

function paypalLogin() {
    executePost3(getAppUrl() + 'signin/paypal', 'acceptTerms', getAcceptTermsVal());
}

function pingIdentityLogin() {
    executeGet3(getAppUrl() + 'saml/' + getCurrentId(), 'acceptTerms', getAcceptTermsVal());
}

function samlLogin() {
    executeGet3(getAppUrl() + 'saml/' + getCurrentId(), 'acceptTerms', getAcceptTermsVal());
}

function oktaLogin() {
    executeGet3(getAppUrl() + 'saml/' + getCurrentId(), 'acceptTerms', getAcceptTermsVal());
}

function oneLoginLogin() {
    executeGet3(getAppUrl() + 'saml/' + getCurrentId(), 'acceptTerms', getAcceptTermsVal());
}

function adfsLogin() {
    executeGet3(getAppUrl() + 'portalsaml/login/' + getCurrentId(), 'acceptTerms', getAcceptTermsVal());
}

function veoliaSamlLogin() {
    executeGet3(getAppUrl() + 'portalsaml/login/' + getCurrentId(), 'acceptTerms', getAcceptTermsVal());
}

function smsreg() {
    var phone_number = $('#sms_self_registration_submit_form #selfregister_sms').val();
    var sms_code = $('#sms_self_registration_submit_form #sms_code').val();

    var params = {};
    params['phone_number'] = phone_number;
    params['sms_code'] = sms_code;
    //if(typeof(analytics) != "undefined") params['analytics'] = analytics;

    executePost2(getAppUrl() + 'signin/smsreg', params);
}

function anonymousreg() {
    executePost3(getAppUrl() + 'signin/anonymousreg', 'acceptTerms', getAcceptTermsVal());
}

function emailOnlyAccess() {

    // Building form action url that will work with custom user domain.
    var form = document.getElementById('email_only_registration_submit_form');
    var customurl = getAppUrl() + 'captivePortal/emailonly/' + getCurrentId();
    form.action = customurl;

    // Creating temporary fields and appending to this form.
    var termsinput = document.createElement('input');
    termsinput.name = 'acceptTerms';
    termsinput.className = "hidden";
    termsinput.value = getAcceptTermsVal();

    var promotionsinput = document.createElement('input');
    promotionsinput.name = 'acceptPromotions';
    promotionsinput.className = "hidden";
    promotionsinput.value = getAcceptPromotionsVal();

    // Adding temporary fields to the form.
    form.appendChild(termsinput);
    form.appendChild(promotionsinput);
    form.setAttribute("method", "POST");

    // Executing POST request
    form.submit();

    return false;
}


function ironwifiLogin() {
//function emailselfregLogin() {	

    // Building form action url that will work with custom user domain.
    var form = document.getElementById('email_self_registration_submit_form');
    var customurl = getAppUrl() + 'signin/emailselfregistration';
    form.action = customurl;

    // Creating temporary fields and appending to this form.
    var termsinput = document.createElement('input');
    termsinput.name = 'acceptTerms';
    termsinput.className = "hidden";
    termsinput.value = getAcceptTermsVal();


    var promotionsinput = document.createElement('input');
    promotionsinput.name = 'acceptPromotions';
    promotionsinput.className = "hidden";
    promotionsinput.value = getAcceptPromotionsVal();

    // Adding temporary fields to the form.
    form.appendChild(termsinput);
    form.appendChild(promotionsinput);
    form.setAttribute("method", "POST");

    // Executing POST request
    form.submit();

    return false;
}

function paidAccess() {

    // Getting selected payment plan.
    /*
     var options = document.getElementById('form1').getElementsByTagName("input");

     var planId = 0;
     for (var i = 0; i < options.length; i++) {
     if (options[i].checked) {
     planId = options[i].value;
     };
     }

     if (planId == 0) {
     if ($('#paypal_express_checkout_select_container select').length) {
     planId = $('#paypal_express_checkout_select_container select').val();
     }
     }

     if (planId == 0) {
     // Cannot get selected pricing plan.
     alert('Please select pricing plan before use PayPal express checkout.');
     }
     */

    var params = {};
    //params['plan'] = planId;

    // Applying CF to request.
    var form = $('#form1');
    form.find('input').each(function () {
        var name = $(this).attr('name');
        var value = $(this).val();
        if ($(this).attr('type') == "radio") {
            if ($(this).is(":checked")) {
                params[name] = value;
            }
        } else {
            params[name] = value;
        }

    });
    params['plan_quantity'] = params['plan'+params['selected_plan']+'_quantity'];

    form.find('select').each(function () {
        var name = $(this).attr('name');
        var value = $(this).val();
        params[name] = value;
    });

    executePost2(getAppUrl() + 'signin/hotspot', params);
}

function paypalPaidAccess() {

    // Getting selected payment plan.
    var options = document.getElementById('paypal_express_checkout').getElementsByTagName("input");

    var planId = 0;
    for (var i = 0; i < options.length; i++) {
        if (options[i].checked) {
            planId = options[i].value;
        }
        ;
    }

    if (planId == 0) {
        if ($('#paypal_express_checkout_select_container select').length) {
            planId = $('#paypal_express_checkout_select_container select').val();
        }
    }

    if (planId == 0) {
        // Cannot get selected pricing plan.
        alert('Please select pricing plan before use PayPal express checkout.');
    }

    var params = {};
    params['plan'] = planId;

    // Applying CF to request.
    var form = $('#expresscheckout_cf');
    form.find('input').each(function () {
        var name = $(this).attr('name');
        var value = $(this).val();
        params[name] = value;
    });

    form.find('select').each(function () {
        var name = $(this).attr('name');
        var value = $(this).val();
        params[name] = value;
    });

    executePost2(getAppUrl() + 'captivePortal/pay', params);
}

function hs2Login() {
    executePost(getAppUrl() + 'captivePortal/hs2proceed/' + getCurrentId());
}

function hs2UnsecureLogin() {
    executePost(getAppUrl() + 'captivePortal/hs2proceed_unsecure/' + getCurrentId());
}

function hs2LoginFromSuccessPage() {

    // Getting current portal id.
    var portalId = location.pathname.split('/')[4];

    executePost(getAppUrl() + 'captivePortal/hs2proceed/' + portalId);
}

function oneTimeAccess() {
    var params = {};
    var email = document.getElementById('ota_email').value;
    params['email'] = email;
    //if(typeof(analytics) != "undefined") params['analytics'] = analytics;
    executePostWithParams(getAppUrl() + 'signin/onetimeaccess', params);
}

function employeeAuthAccess() {
    var params = {};
    var fullName = document.getElementById('eaa_fullname').value;
    params['firstname'] = fullName.split(' ').slice(0, -1).join(' ');
    params['lastname'] = fullName.split(' ').slice(-1).join(' ');
    params['email'] = document.getElementById('eaa_email').value;
    //if(typeof(analytics) != "undefined") params['analytics'] = analytics;
    executePostWithParams(getAppUrl() + 'signin/employeeauth', params);
}


function voucherAccess() {

    var voucher = $('#vouchers_form #voucher').val();

    var params = {};
    params['voucher'] = voucher;
    //if(typeof(analytics) != "undefined") params['analytics'] = analytics;

    executePost2(getAppUrl() + 'signin/voucher', params);
}

function emailSelfRegLogin() {

    // Building form action url that will work with custom user domain.
    var form = document.getElementById('email_self_registration_submit_form');
    var customurl = getAppUrl() + 'signin/emailselfregistration';
    form.action = customurl;

    // Creating temporary fields and appending to this form.
    var termsinput = document.createElement('input');
    termsinput.name = 'acceptTerms';
    termsinput.className = "hidden";
    termsinput.value = getAcceptTermsVal();


    var promotionsinput = document.createElement('input');
    promotionsinput.name = 'acceptPromotions';
    promotionsinput.className = "hidden";
    promotionsinput.value = getAcceptPromotionsVal();

    // Adding temporary fields to the form.
    form.appendChild(termsinput);
    form.appendChild(promotionsinput);
    form.setAttribute("method", "POST");

    // Executing POST request
    form.submit();

    var fel = $('#email_self_registration_submit_form');
    fel.on('onsubmit', false);

    return false;
}

function uapLogin() {

    var form = document.getElementById('uap_submit_form');
    var customurl = getAppUrl() + 'accessRequest/request';
    form.action = customurl;

    // Removing all previous errors from page.
    $('#error_container').addClass('hidden');

    // Validating UAP form
    if ($('#uap_username').val().length == 0) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('First name is required.');

        return false;
    }

    if ($('#uap_useremail').val().length == 0) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Enter your email address.');

        return false;
    } else if (!isValidEmailAddress($('#uap_useremail').val())) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Invalid email address format.');

        return false;
    }

    if ($('#uap_hostemail').val().length == 0) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Enter host email address.');

        return false;
    } else if (!isValidEmailAddress($('#uap_hostemail').val())) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Invalid host email address format.');

        return false;
    }

    // Creating temporary fields and appending to this form.
    var termsinput = document.createElement('input');
    termsinput.name = 'acceptTerms';
    termsinput.className = "hidden";
    termsinput.value = getAcceptTermsVal();

    // Adding temporary fields to the form.
    form.appendChild(termsinput);
    form.setAttribute("method", "POST");
    form.submit();
    return false;
}

function osuLogin() {

    var form = document.getElementById('onlinesignup_form');
    var customurl = getAppUrl() + 'onlinesignup';
    form.action = customurl;

    // Removing all previous errors from page.
    $('#error_container').addClass('hidden');

    // Validating OSU form
    if ($('#user_name').val().length == 0) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('First name is required.');

        return false;
    }

    if ($('#user2name').val().length == 0) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Last name is required.');

        return false;
    }

    if ($('#user_mail').val().length == 0) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Enter your email address.');

        return false;
    } else if (!isValidEmailAddress($('#user_mail').val())) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Invalid email address format.');

        return false;
    }

    /*if (getAcceptTermsVal() == "notaccepted") {
     $('#error_container').removeClass('hidden');
     $('#error_inner_container').html('Please accept portal Terms&Conditions.');

     return false;
     }*/

    // Adding temporary fields to the form.
    form.setAttribute("method", "POST");
    form.submit();
    return false;
}

function customerOSUlogin() {

    var form = document.getElementById('onlinesignup_form');
    var customurl = getAppUrl() + 'onlinesignup';
    form.action = customurl;

    // Removing all previous errors from page.
    $('#error_container').addClass('hidden');

    // Validating OSU form
    if ($('#user_name').val().length == 0) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('First name is required.');

        return false;
    }

    if ($('#user2name').val().length == 0) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Last name is required.');

        return false;
    }

    if ($('#user_mail').val().length == 0) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Enter your email address.');

        return false;
    } else if (!isValidEmailAddress($('#user_mail').val())) {

        // User name should not be empty.
        $('#error_container').removeClass('hidden');
        $('#error_inner_container').html('Invalid email address format.');

        return false;
    }

    /*if (getAcceptTermsVal() == "notaccepted") {
     $('#error_container').removeClass('hidden');
     $('#error_inner_container').html('Please accept portal Terms&Conditions.');

     return false;
     }*/

    // Adding temporary fields to the form.
    form.setAttribute("method", "POST");
    form.setAttribute("action", location.pathname);

    form.submit();
    return false;
}

function guestSelfRegUserValidate() {
    var form = $('#email_guest_self_registration_submit_form');

    // Error container.
    var errcont = $('#error_container');
    if (errcont.length) {
        errcont.addClass('hidden');
    }

    var err = $('#error_inner_container');
    if (err.length) {
        err.html('');
    }

    // Validating user email.
    var emailfield = form.find('#guestselfregister_email');
    if (emailfield.length) {
        var email = emailfield.val();
        if (email.length == 0) {
            errcont.removeClass('hidden');
            err.html('Email address is required.');
            return;
        } else if (!isValidEmailAddress(email)) {
            errcont.removeClass('hidden');
            err.html('Invalid email address format');
            return;
        }
    }

    guestSelfRegUserRegister();
}

function guestSelfRegUserRegister() {
    var form = $('#email_guest_self_registration_submit_form');
    var params = {};
    //var fullName = form.find('#guestselfregister_fullname').val();
    //params['firstname'] = fullName.split(' ').slice(0, -1).join(' ');
    //params['lastname'] = fullName.split(' ').slice(-1).join(' ');
    //params['mobilephone'] = form.find('#guestselfregister_mobilephone').val();
    //params['email'] = form.find('#guestselfregister_email').val();
    //if(typeof(analytics) != "undefined") params['analytics'] = analytics;

    $("form#email_guest_self_registration_submit_form :input").each(function () {
        params[$(this).attr('name')] = $(this).val();
    });

    $('form#email_guest_self_registration_submit_form input:checked').each(function () {
        params[$(this).attr('name')] = 'on';
    });

    $('form#email_guest_self_registration_submit_form input:checkbox:not(:checked)').each(function () {
        params[$(this).attr('name')] = 'off';
    });

    var path = getAppUrl() + 'signin/guestselfregister';
    executePost2(path, params);
}

function selfRegUserValidate() {
    var form = $('#email_self_registration_submit_form');

    // Error container.
    var errcont = $('#error_container');
    if (errcont.length) {
        errcont.addClass('hidden');
    }

    var err = $('#error_inner_container');
    if (err.length) {
        err.html('');
    }

    // Validating user email.
    var emailfield = form.find('#selfregister_email');
    if (emailfield.length) {
        var email = emailfield.val();
        if (email.length == 0) {
            errcont.removeClass('hidden');
            err.html('Email address is required.');
            return;
        } else if (!isValidEmailAddress(email)) {
            errcont.removeClass('hidden');
            err.html('Invalid email address format');
            return;
        }
    }

    var passwordfield = form.find('#selfregister_clear_password');
    if (passwordfield.length) {
        var pwd = passwordfield.val();
        if (pwd.length == 0) {
            errcont.removeClass('hidden');
            err.html('Password is required.');
            return;
        }
    }

    selfRegUserRegister();
}

function selfRegUserRegister() {
    var form = $('#email_self_registration_submit_form');

    var params = {};
    var fullName = form.find('#selfregister_fullname').val();
    params['firstname'] = fullName.split(' ').slice(0, -1).join(' ');
    params['lastname'] = fullName.split(' ').slice(-1).join(' ');
    params['email'] = form.find('#selfregister_email').val();
    params['password'] = form.find('#selfregister_clear_password').val();
    //if(typeof(analytics) != "undefined") params['analytics'] = analytics;

    var path = getAppUrl() + 'signin/selfregister';

    executePost2(path, params);
}

function localaccount() {
    var form = $('#localaccount_submit_form');

    var params = {};
    params['username'] = form.find('#localaccount_username').val();
    params['password'] = form.find('#localaccount_clear_password').val();
    //if(typeof(analytics) != "undefined") params['analytics'] = analytics;

    var path = getAppUrl() + 'signin/localaccount';


    executePost2(path, params);
}

function reaceptTerms() {

    var portalId = getCurrentIdUn();
    var params = {};

    executePost2(getAppUrl() + 'captivePortal/reacepttermsconfirm/' + portalId, params);
}

function executePost(path) {

    var form = document.createElement("form");
    form.setAttribute("method", "POST");
    form.setAttribute("action", path);

    if (typeof(analytics) != "undefined") {
        var input = document.createElement('input');
        input.name = 'analytics';
        input.value = analytics;
        form.appendChild(input);
    }

    document.body.appendChild(form);

    form.submit();
    document.body.removeChild(form);
}


function executePost3(path, paramname, paramvalue) {

    var form = document.createElement("form");
    form.setAttribute("method", "POST");
    form.setAttribute("action", path);

    // Create an input element, and append it to the form:
    var input = document.createElement('input');
    input.name = paramname;
    input.value = paramvalue;
    form.appendChild(input);

    if (typeof(analytics) != "undefined") {
        var input = document.createElement('input');
        input.name = 'analytics';
        input.value = analytics;
        form.appendChild(input);
    }

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}


function executePost2(path, params) {

    var form = document.createElement("form");
    form.setAttribute("method", "POST");
    form.setAttribute("action", path);

    for (var key in params) {

        // Create an input element, and append it to the form.
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = params[key];
        form.appendChild(input);
    }

    if (typeof(analytics) != "undefined") {
        var input = document.createElement('input');
        input.name = 'analytics';
        input.value = analytics;
        form.appendChild(input);
    }

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}


function executeGet3(path, param1, value1) {
    var loc = path + '?' + param1 + '=' + value1;
    //if(typeof(analytics) != "undefined"){
    //	loc = loc + '&analytics=' + encodeURIComponent(analytics);
    //}
    window.location = loc;
}

function executeGet5(path, param1, value1, param2, value2) {
    var loc = path + '?' + param1 + '=' + value1 + '&' + param2 + '=' + value2;
    //if(typeof(analytics) != "undefined"){
    //	loc = loc + '&analytics=' + encodeURIComponent(analytics);
    //}
    window.location = loc;
}

function selectFirstPaymentPlan() {
    var allElems = document.getElementsByName('plan');
    if (allElems.length > 0) {
        allElems[0].checked = true;
    }
    ;
}

//Function to read cookie value from user session.			
function getCookie(c_name) {
    var c_value = document.cookie;
    var c_start = c_value.indexOf(" " + c_name + "=");
    if (c_start == -1) {
        c_start = c_value.indexOf(c_name + "=");
    }
    if (c_start == -1) {
        c_value = null;
    } else {
        c_start = c_value.indexOf("=", c_start) + 1;
        var c_end = c_value.indexOf(";", c_start);
        if (c_end == -1) {
            c_end = c_value.length;
        }
        c_value = unescape(c_value.substring(c_start, c_end));
    }
    return c_value;
}

// Function to add cookie to user session.
function setCookie(c_name, value, exdays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value = escape(value) + ((exdays == null) ? "" : "; expires=" + exdate.toUTCString());
    document.cookie = c_name + "=" + c_value;
}

function delete_cookie( name ) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/';
}

function changeLang() {

    var e = document.getElementById("lang_select");
    var val = e.options[e.selectedIndex].value;

    if (gup('lang') == val) {
        // This language already selected.
        return;
    }

    var base = location.protocol + '//' + location.host + location.pathname;

    // Reloading page with requested language
    window.location = base + '?lang=' + val;
}

// Get attribute value from request URL.
function gup(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.href);
    if (results == null) {
        return "";
    } else {
        return results[1];
    }
}
/**
 * Initialize actions of fields for 'Email Self Registration' authentication provider.
 * Should be called on load of document.
 */
function initSelfRegActions() {

    var el = $('#selfreg_email');
    if (!hasPlaceholder(el)) {
        el.attr('placeholder', 'Email');
    }

    if ($('#selfreg_clear_password').length) {

        // Hide special clear text password field.
        $('#selfreg_clear_password').hide();
    }

    if ($('#selfreg_password').length) {

        var el = $('#selfreg_password');
        el.show();

        if (!hasPlaceholder(el)) {
            el.attr('placeholder', 'Password');
        }
    }
}

/**
 * Initialize actions of fields for 'Email Only Registration' authentication provider.
 * Should be called on load of document.
 */
function initEmailOnlyActions() {

    var fn = $('#emailonly_firstname');
    if (!hasPlaceholder(fn)) {
        fn.attr('placeholder', 'First Name');
    }

    var ln = $('#emailonly_lastname');
    if (!hasPlaceholder(ln)) {
        ln.attr('placeholder', 'Last Name');
    }

    var email = $('#emailonly_email');
    if (!hasPlaceholder(email)) {
        email.attr('placeholder', 'Email');
    }
}

function initRegFormActions() {
    $('#selfregister_firstname').attr('placeholder', 'First Name');
    $('#selfregister_lastname').attr('placeholder', 'Last Name');
    $('#selfregister_email').attr('placeholder', 'Email');
    $('#selfregister_clear_password').show();
    $('#selfregister_password').hide();

    $('#selfregister_clear_password').focus(function () {
        $('#selfregister_clear_password').hide();
        $('#selfregister_password').show();
        $('#selfregister_password').focus();
    });
    $('#selfregister_password').blur(function () {
        if ($('#selfregister_password').val() == '') {
            $('#selfregister_clear_password').show();
            $('#selfregister_password').hide();
        }
    });
    $('#selfregister_firstname').focus(function () {
        $('#selfregister_firstname').attr('placeholder', '');
    });
    $('#selfregister_firstname').blur(function () {
        $('#selfregister_firstname').attr('placeholder', 'First Name');
    });
    $('#selfregister_lastname').focus(function () {
        $('#selfregister_lastname').attr('placeholder', '');
    });
    $('#selfregister_lastname').blur(function () {
        $('#selfregister_lastname').attr('placeholder', 'Last Name');
    });
    $('#selfregister_email').focus(function () {
        $('#selfregister_email').attr('placeholder', '');
    });
    $('#selfregister_email').blur(function () {
        $('#selfregister_email').attr('placeholder', 'Email');
    });
}

function getAppUrl() {

    var path = location.pathname.split('/');
    var app = path[1];

    var fullAppUrl = location.protocol + '//' + location.hostname +
        (location.port ? ':' + location.port : '') + '/' + app + '/';

    //var fullAppUrl = location.protocol + '//' + location.hostname + 
    //		(location.port ? ':'+location.port: '') + '/';

    return fullAppUrl;
}

function deleteCredentials() {
    var path = location.pathname.split('/');
    var cp_id = path[3];

    delete_cookie('auth_user_'+cp_id);
    delete_cookie('auth_pass_'+cp_id);

    console.log('cookie deleted'+'auth_user_'+cp_id);

    var target_url = getAppUrl()+'pages/'+cp_id+'/';
    console.log('redirecting to: '+target_url);
    window.location = target_url;

    return true;
}

function getCurrentId() {

    var path = location.pathname.split('/');

    if (path.length > 2) {
        return path[2];
    } else {
        return 0;
    }
    ;
}

// Universal type of function 'getCurrentId'
function getCurrentIdUn() {

    var path = location.pathname.split('/');

    if (path.length > 2) {

        var id = path[2];

        if (isNaN(id)) {
            if (path.length > 3) {
                id = path[3];

                if (!isNaN(id)) {
                    return id;
                }
            }
        } else {
            return id;
        }
    }

    return 0;
}


/**
 * Get if user clicked on 'Accept Terms&Conditions' check box.
 * @returns 'accepted' - if user have accepted Terms.
 *            'notaccepted' - in other case.
 */
function termsChecked() {
    var acceptterms = document.getElementById('terms');
    var state;
    if (acceptterms.checked == 1) {
        state = 0;
    } else {
        state = 1;
    }
    document.getElementById('terms').checked = state;
    document.getElementById('accept_terms_social_container').checked = state;
    document.getElementById('accept_terms_onetimeaccess_container').checked = state;
    document.getElementById('accept_terms_emailselfreg_container').checked = state;
    document.getElementById('accept_terms_emailonlyreg_container').checked = state;
    document.getElementById('accept_terms_anonymousreg_container').checked = state;
    document.getElementById('accept_terms_smsreg_container').checked = state;
    document.getElementById('accept_terms_vouchers_container').checked = state;
    document.getElementById('accept_terms_paypalcheckout_container').checked = state;
}

function uapTermsChecked() {
    var acceptterms = document.getElementById('terms');
    var state;
    if (acceptterms.checked == 1) {
        state = 0;
    } else {
        state = 1;
    }
    document.getElementById('terms').checked = state;
    document.getElementById('accept_terms_container').checked = state;
}

function getAcceptTermsVal() {

    var acceptterms = document.getElementById('terms');
    var value = "notaccepted";
    if (acceptterms) {
        if (acceptterms.checked == 1) {
            value = "accepted";
        }
        ;
    }
    ;

    return value;
}

/**
 * Get if user clicked on 'Accept Promotions' check box.
 * @returns 'accepted' - if user have accepted Terms.
 *            'notaccepted' - in other case.
 */
function promotionsChecked() {
    var acceptpromotions = document.getElementById('accept_promotions_chbox');
    var state;
    if (acceptpromotions.checked == 1) {
        state = 0;
    } else {
        state = 1;
    }
    document.getElementById('accept_promotions_chbox').checked = state;
    document.getElementById('accept_promotions_social_container').checked = state;
    document.getElementById('accept_promotions_onetimeaccess_container').checked = state;
    document.getElementById('accept_promotions_emailselfreg_container').checked = state;
    document.getElementById('accept_promotions_emailonlyreg_container').checked = state;
    document.getElementById('accept_promotions_anonymousreg_container').checked = state;
    document.getElementById('accept_promotions_smsreg_container').checked = state;
    document.getElementById('accept_promotions_vouchers_container').checked = state;
    document.getElementById('accept_promotions_paypalcheckout_container').checked = state;
}

function uapPromotionsChecked() {
    var acceptpromotions = document.getElementById('accept_promotions_chbox');
    var state;
    if (acceptpromotions.checked == 1) {
        state = 0;
    } else {
        state = 1;
    }
    document.getElementById('accept_promotions_chbox').checked = state;
    document.getElementById('accept_promotions_container').checked = state;
}

function getAcceptPromotionsVal() {

    var acceptpromotions = document.getElementById('accept_promotions_chbox');
    var value = "notpromoaccepted";
    if (acceptpromotions) {
        if (acceptpromotions.checked == 1) {
            value = "promoaccepted";
        }
        ;
    }
    ;

    return value;
}

/**
 * Get if user clicked on 'Accept Promotions' check box.
 * @returns 'accepted' - if user have accepted Terms.
 *            'notaccepted' - in other case.
 */
function promotionsChecked() {
    var acceptpromotions = document.getElementById('accept_promotions_chbox');
    var state;
    if (acceptpromotions.checked == 1) {
        state = 0;
    } else {
        state = 1;
    }
    document.getElementById('accept_promotions_chbox').checked = state;
    document.getElementById('accept_promotions_social_container').checked = state;
    document.getElementById('accept_promotions_onetimeaccess_container').checked = state;
    document.getElementById('accept_promotions_emailselfreg_container').checked = state;
    document.getElementById('accept_promotions_emailonlyreg_container').checked = state;
    document.getElementById('accept_promotions_anonymousreg_container').checked = state;
    document.getElementById('accept_promotions_smsreg_container').checked = state;
    document.getElementById('accept_promotions_vouchers_container').checked = state;
    document.getElementById('accept_promotions_paypalcheckout_container').checked = state;
}

function uapPromotionsChecked() {
    var acceptpromotions = document.getElementById('accept_promotions_chbox');
    var state;
    if (acceptpromotions.checked == 1) {
        state = 0;
    } else {
        state = 1;
    }
    document.getElementById('accept_promotions_chbox').checked = state;
    document.getElementById('accept_promotions_container').checked = state;
}

function getAcceptPromotionsVal() {

    var acceptpromotions = document.getElementById('accept_promotions_chbox');
    var value = "notpromoaccepted";
    if (acceptpromotions) {
        if (acceptpromotions.checked == 1) {
            value = "promoaccepted";
        }
        ;
    }
    ;

    return value;
}

function getScreenSize() {
    var height = window.screen.height * window.devicePixelRatio;
    var width = window.screen.width * window.devicePixelRatio;
    return width + 'x' + height;
}
function setScreenSizeIntoField() {
    document.getElementById('screenSize').value = getScreenSize();
}

//If HS 2.0 enabled - check IPad version and show 
//'HS 2.0 login button only for devices > 2 version.'
function checkIpadVersion() {
    window.ondevicemotion = function (event) {
        if (navigator.platform.indexOf("iPad") != -1) {
            var version = 1;
            if (event.acceleration) version += window.devicePixelRatio;

            if (version > 2) {
                // Show HS2 secure login button
                $("#secure_access").removeClass('hidden');
            }
        } else if (navigator.platform.indexOf("iPhone") != -1) {
            var iHeight = window.screen.height;

            if (iHeight > (960 / 2)) {
                // It's iPhone 5. Showing HS2.0 secure login button.
                $("#secure_access").removeClass('hidden');
            }
        }
        window.ondevicemotion = null;
    };
}

function validateOTAForm() {
    var re_email = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    var emailAddress = $('#ota_email').val();
    var placeholder_email = $('#ota_email').attr("placeholder");

    if (emailAddress.length < 1 || emailAddress == placeholder_email || !re_email.test(emailAddress) || emailAddress.indexOf('+') > -1) {
        // needs to be replaced with code to show an error message
        $("#popupErrorConfirmEmailAddressFormat").popup("open", {transition: "fade", history: false});
        return false;
    }
    else {
        return oneTimeAccess();
    }
}

function validateVouchersForm() {
    var voucher = $('#voucher').val();
    var placeholder_voucher = $('#voucher').attr("placeholder");

    if (voucher.length < 1 || voucher == placeholder_voucher) {
        // needs to be replaced with code to show an error message
        $("#popupErrorConfirmEmailAddressFormat").popup("open", {transition: "fade", history: false});
        return false;
    }
    else {
        return voucherAccess();
    }
}

function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return pattern.test(emailAddress);
}

/**
 * Check that element has 'placeholder' attribute and its value is not empty.
 * @param el - jquery element.
 */
function hasPlaceholder(el) {
    var ph = el.attr('placeholder');
    if (typeof ph !== typeof undefined && ph !== false) {
        if (el.attr('placeholder') !== '') {
            return true;
        }
    }
    return false;
}

/**
 * Check if request was approved.
 */
function checkRequestApproved() {

    setInterval(function () {

        var id = $('#requestId').html();
        var url = getAppUrl() + 'accessRequest/check?id=' + id;

        $.ajax({
            url: url,
            cache: false,
            type: 'GET',
            async: false,
            success: function (response) {

                if (response == 'true' || response == true || response == 'Accepted') {
                    var portalId = $('#portalId').html();
                    var continueUrl = getAppUrl() + 'accessRequest/continue/' + portalId + '?id=' + id;
                    window.location = continueUrl;
                } else if (response == 'rejected' || response == 'Rejected') {
                    var portalId = $('#portalId').html();
                    var continueUrl = getAppUrl() + 'accessRequest/rejected/' + portalId + '?id=' + id;
                    window.location = continueUrl;
                }
            }
        });
    }, 5000);
}

// Grant access for user access request
function grantAccess() {

    // Prepearing parameters.
    var token = $('#token').html();

    var period = $('#period').val();
    var rate = $('#rate').val();

    var continueUrl = getAppUrl() + 'accessRequest/approve_confirm?token=' + token + '&period=' + period + '&rate=' + rate;

    window.location = continueUrl;
}

// Delete user access request
function deleteRequest() {

    // Prepearing parameters.
    var token = $('#token').html();
    var portalid = $('#portalid').html();

    var continueUrl = getAppUrl() + 'accessRequest/delete_request';
    executeGet5(continueUrl, 'token', token, 'portalid', portalid);
}

function reRequestAccess() {
    var portalId = $('#portalId').html();
    var continueUrl = getAppUrl() + 'captivePortal/' + portalId;
    window.location = continueUrl;
}

function uapCloseDelWindow() {
    document.getElementById('myPopup').style.visibility = 'hidden';
    parent.location.hash = '';
}

function changeAgeDefault() {
    $("select[name='userAge'] option").each(function () {
        if ($(this).text().indexOf("Not Answered") >= 0) {
            $(this).text('Select your age range');
        } else {
            $(this).text($(this).text() + ' years old');
        }
    });

    $('select[name="userAge"]').prev().text('Select your age range');
}

function sendErrorRedirect(splashPageUrl, errorMessage) {
    var redirectUrl = splashPageUrl;
    if (redirectUrl.indexOf("?") != -1) {
        redirectUrl += "&";
    } else {
        redirectUrl += "?";
    }
    redirectUrl += "error=true";
    errorMessage = encodeURIComponent(errorMessage);
    redirectUrl += "&error_msg=" + errorMessage;
    window.location = redirectUrl;
}

function startCiscoSessionPoll(endpoint, retries, timeout, successUrl, failureUrl) {
    startSessionPoll(endpoint, retries, timeout, "authenticated", successUrl, failureUrl);
}

function startSessionPoll(endpoint, retries, timeout, authState, successUrl, failureUrl) {
    var settings = {
        url: endpoint,
        error: function (xhr, status, reason) {
            sendErrorRedirect(failureUrl,
                "Error while polling user session. Reason: " + reason);
        }
    };
    var success = function (session, status, xhr) {
        if (session.state == authState) {
            window.location = successUrl;
            return false;
        }
        return true;
    };
    var finish = function (attempts, retries, delay) {
        if (attempts >= retries) {
            sendErrorRedirect(failureUrl,
                "User authentication failed to complete within the specified time.");
        }
    };
    startAjaxPoll(settings, retries, timeout, success, finish);
}

function startAjaxPoll(settings, retries, delay, success, finish) {
    doAjaxPoll(settings, 0, retries, delay, success, finish);
}

function doAjaxPoll(settings, attempts, retries, delay, success, finish) {

    if (attempts > retries) {
        return;
    }

    $.ajax(settings).success(
        function (data, status, xhr) {
            var keepGoing = success(data, status, xhr);
            if (attempts < retries && keepGoing) {
                setTimeout(function () {
                    doAjaxPoll(settings, attempts + 1,
                        retries, delay, success, finish);
                }, delay);
            } else {
                finish(attempts, retries, delay);
            }
        }
    );
}

function executePostWithParams(path, params) {

    var form = document.createElement("form");
    form.setAttribute("method", "POST");
    form.setAttribute("action", path);

    for (var key in params) {
        // Create an input element, and append it to the form.
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = params[key];
        form.appendChild(input);
    }

    if (typeof(analytics) != "undefined") {
        var input = document.createElement('input');
        input.name = 'analytics';
        input.value = analytics;
        form.appendChild(input);

        if (typeof(fingerprint) != "undefined") {
            var input = document.createElement('input');
            input.name = 'fingerprint';
            input.value = fingerprint;
            form.appendChild(input);
        }
    }

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}