import { AbstractControl, ValidationErrors, ValidatorFn } from "@angular/forms";

export const passwordValidator: ValidatorFn = (
    control: AbstractControl,
): ValidationErrors | null => {
    const password = control.get('password');
    const confirmPassword = control.get('confirm_password');

    return password && confirmPassword && password.value !== confirmPassword.value
        ? { passwordDoesNotMatch : true }
        : null;
};