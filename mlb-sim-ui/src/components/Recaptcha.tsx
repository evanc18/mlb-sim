import React, { useEffect, useState } from 'react';

interface RecaptchaProps {
    sitekey: string;
    onVerify: (response: string) => void;
}

const Recaptcha: React.FC<RecaptchaProps> = ({ sitekey, onVerify }) => {
    const [loaded, setLoaded] = useState(false);

    useEffect(() => {
        const script = document.createElement('script');
        script.src = `https://www.google.com/recaptcha/api.js?render=${sitekey}`;
        script.addEventListener('load', () => setLoaded(true));
        document.head.appendChild(script);

        return () => {
            document.head.removeChild(script);
        };
    }, [sitekey]);

    const handleVerify = (token: string) => {
        onVerify(token);
    };

    return (
        <div className="g-recaptcha" data-sitekey={sitekey}></div>
    );
};

export default Recaptcha;