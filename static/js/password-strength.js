jQuery(() => {
  const $passwordInput = jQuery('input[type="password"]');
  const $passwordAlert = jQuery('.password-alert');
  const $form = jQuery('form');
  const $requirements = jQuery('.requirements');

  let hasMinLength, hasUppercase, hasNumbers, hasSpecials;

  const $length = jQuery('.length');
  const $bigLetter = jQuery('.big-letter');
  const $numbers = jQuery('.numbers');
  const $specialChar = jQuery('.special-char');

  $requirements.addClass('wrong');

  $passwordInput.on('focus', () => {
    $passwordAlert.show();
  });

  $form.on('submit', () => {
    const input = document.querySelector('input[type="password"]');

    const isInputValid = input.checkValidity();

    if (!isInputValid) {
      input.reportValidity();

      return false;
    }

    if (hasMinLength && hasUppercase && hasNumbers && hasSpecials) {
      input.reportValidity();

      return true;
    }

    return false;
  });

  $passwordInput.on('input blur', (e) => {
    const inputElement = jQuery(e.target);

    const inputValue = inputElement.val();

    $passwordAlert.show();

    hasMinLength = inputValue.length > 7 && inputValue.length < 48;

    hasUppercase = inputValue.toLowerCase() !== inputValue;

    hasNumbers = /\d/.test(inputValue);

    hasSpecials = /^[\w!@#$%^*()_+\-=\[\]{};\\|,.<>\/?]+$/.test(inputValue);

    if (hasMinLength && hasUppercase && hasNumbers && hasSpecials) {
      jQuery(this).addClass('valid').removeClass('invalid');

      $requirements.removeClass('wrong').addClass('good');
      $passwordAlert.removeClass('alert-warning').addClass('alert-success');
    } else {
      jQuery(this).addClass('invalid').removeClass('valid');

      $passwordAlert.removeClass('alert-success').addClass('alert-warning');

      if (hasMinLength === false) {
        $length.addClass('wrong').removeClass('good');
      } else {
        $length.addClass('good').removeClass('wrong');
      }

      if (hasUppercase === false) {
        $bigLetter.addClass('wrong').removeClass('good');
      } else {
        $bigLetter.addClass('good').removeClass('wrong');
      }

      if (hasNumbers === false) {
        $numbers.addClass('wrong').removeClass('good');
      } else {
        $numbers.addClass('good').removeClass('wrong');
      }

      if (hasSpecials === false) {
        $specialChar.addClass('wrong').removeClass('good');
      } else {
        $specialChar.addClass('good').removeClass('wrong');
      }
    }

    if (e.type === 'blur') {
      $passwordAlert.hide();
    }
  });
});