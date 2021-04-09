import React, {useCallback, useEffect, useRef, useState} from 'react';
import {SETTINGS} from '../settings';
import Cookies from 'js-cookie';


const UserRow = ({user}) => {
    return (
        <tr key={`user_${user.id}`}>
            <td>{user.name}</td>
            <td>{user.password}</td>
            <td>{user.created_at}</td>
            <td>{user.active ? 'yes' : 'no'}</td>
        </tr>
    );
};

const AdminUser = () => {
        const usernameInput = useRef(null);
        const [adminUserData, setAdminUserData] = useState(null);
        useEffect(() => {
            const token = Cookies.get(SETTINGS.AUTH_TOKEN_NAME);

            async function a() {
                const res = await fetch('http://127.0.0.1:3000/api/user/demo-admin', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    }
                });
                if (res.status === 200) {
                    const data = await res.json();
                    console.log("HERE", data);
                    setAdminUserData(data);
                } else {
                    const text = await res.text();
                    setAdminUserData({status: res.status, text});
                }
            }

            a();
        }, []);

        const createUser = useCallback(async () => {
            const username = usernameInput.current.value;
            if (!username) {
                alert("Can not create a user without a name")
            } else {
                const data = {
                    name: username,
                }
                const token = Cookies.get(SETTINGS.AUTH_TOKEN_NAME);
                const res = await fetch('http://127.0.0.1:3000/api/user/demo-admin', {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                if (res.status === 201) {
                    const data = await res.json()
                    setAdminUserData({
                        status: adminUserData.status,
                        data: [...adminUserData.data, data.data]
                    });
                }
            }
        }, [adminUserData])

        return (
            <>
                <p>Admin User response: {adminUserData?.status}</p>
                <input type="text" placeholder="username" name="username" ref={usernameInput}/>
                <button type="button" onClick={createUser}>Create user</button>
                {adminUserData?.status === 'ok' && (
                    <table>
                        <thead>
                        <tr>
                            <th>Username</th>
                            <th>Password</th>
                            <th>Created At</th>
                            <th>Active</th>
                        </tr>
                        </thead>
                        <tbody>
                        {
                            adminUserData.data.map((user => <UserRow user={user} />))
                        }
                        </tbody>

                    </table>
                )}
            </>
        );
    }
;

export default AdminUser;
