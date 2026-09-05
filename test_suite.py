import urllib.request
import json

def run_tests():
    # 1. Test GET /
    req = urllib.request.urlopen('http://127.0.0.1:5000/')
    html = req.read().decode('utf-8')
    assert req.status == 200, f'Status: {req.status}'
    assert 'resume-modal' in html, 'resume-modal missing in HTML'
    assert 'project-modal' in html, 'project-modal missing in HTML'
    assert 'filter-btn' in html, 'filter-btn missing in HTML'
    assert 'toast-notice' in html, 'toast-notice missing in HTML'
    assert 'og:title' in html, 'og:title missing in HTML'
    print('[PASS] GET /: Loaded successfully with all 5 improvements present in DOM.')

    # 2. Test GET /api/portfolio-data
    req2 = urllib.request.urlopen('http://127.0.0.1:5000/api/portfolio-data')
    data = json.loads(req2.read().decode('utf-8'))
    assert data['success'] is True
    assert data['data']['profile']['name'] == 'Dharam Jai Vardhan Reddy'
    print('[PASS] GET /api/portfolio-data: Returned valid editable portfolio data.')

    # 3. Test POST /api/contact
    post_data = json.dumps({
        'name': 'Sarah Connor (Talent Partner)',
        'email': 'sarah@globaltech.com',
        'subject': 'Software Engineering Internship / Full-Time Interview',
        'message': 'Hi Dharam, we were very impressed by your IoT and Data Analytics portfolio and would love to interview you for our team.'
    }).encode('utf-8')

    req3 = urllib.request.Request(
        'http://127.0.0.1:5000/api/contact',
        data=post_data,
        headers={'Content-Type': 'application/json'}
    )
    res3 = urllib.request.urlopen(req3)
    contact_res = json.loads(res3.read().decode('utf-8'))
    assert contact_res['success'] is True
    print('[PASS] POST /api/contact: Successfully saved contact message via parameterized SQL.')

    # 4. Test GET /api/messages
    req4 = urllib.request.urlopen('http://127.0.0.1:5000/api/messages')
    msg_data = json.loads(req4.read().decode('utf-8'))
    assert msg_data['success'] is True
    assert msg_data['count'] > 0
    print(f'[PASS] GET /api/messages: Retrieved {msg_data["count"]} contact messages from SQLite database.')

if __name__ == '__main__':
    run_tests()
