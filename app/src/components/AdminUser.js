import React, {useEffect, useState} from 'react';

const AdminUser = () => {
    const [adminUserData, setAdminUserData] = useState(null)
    useEffect(() => {
        async function a () {
            const res = await fetch('http://127.0.0.1:3000/auth/user/demo-admin')
            if (res.status === 200) {
                setAdminUserData(await res.text())
            } else {
                setAdminUserData(await res.text())
            }
        }
        a()
    });
    return (
        <p>Admin User response: {adminUserData}</p>
    );
};

export default AdminUser;
