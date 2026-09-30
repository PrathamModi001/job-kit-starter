async (page) => {
    await page.locator('input#resume').setInputFiles('/home/modi/Work/job-kit-starter/job-kit-starter/output/Yext - Software Engineer/Pratham_Modi_Resume.pdf');
    const files = await page.locator('input#resume').evaluate(el => el.files.length > 0 ? el.files[0].name : 'none');
    return 'File attached: ' + files;
}
