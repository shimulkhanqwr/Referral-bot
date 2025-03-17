function copyReferralLink() {
    var copyText = document.querySelector("#referralLink a");
    var textArea = document.createElement("textarea");
    textArea.value = copyText.href;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    document.body.removeChild(textArea);
    alert("Referral link copied to clipboard!");
}
