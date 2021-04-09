import React, {useEffect, useState} from 'react';
import {SETTINGS} from '../settings';
import Cookies from 'js-cookie';

const AdminUser = () => {
    const [adminUserData, setAdminUserData] = useState(null)
    useEffect(() => {
        const token = Cookies.get(SETTINGS.AUTH_TOKEN_NAME)
        async function a () {
            const res = await fetch('http://127.0.0.1:3000/api/user/demo-admin', {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            })
            if (res.status === 200) {
                const data = await res.json()
                console.log("HERE", data);
                setAdminUserData(data.status)
            } else {
                setAdminUserData(await res.text())
            }
        }
        a()
    }, []);
    return (
        <p>Admin User response: {adminUserData}</p>
    );
};

export default AdminUser;
