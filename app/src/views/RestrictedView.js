import React from 'react';
import { Helmet } from 'react-helmet-async';
import { Row, Col } from 'reactstrap';

import withView from 'decorators/withView';
import { loginRequired } from 'decorators/permissions';
import AdminUser from '../components/AdminUser';

const Restricted = () => (
    <div className="page-container">
        <Helmet title="Example" />

        <Row>
            <Col md={12}>
                <AdminUser />
            </Col>
        </Row>
    </div>
);

const RestrictedView = withView()(loginRequired()(Restricted));

export default RestrictedView;
