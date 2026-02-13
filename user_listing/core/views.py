from django.shortcuts import render

def user_list(request):
    users = [
        {'id': 1, 'name': 'Aarav Patel', 'email': 'aarav.patel@example.com', 'role': 'Developer'},
        {'id': 2, 'name': 'Vihaan Rao', 'email': 'vihaan.rao@example.com', 'role': 'Designer'},
        {'id': 3, 'name': 'Aditya Sharma', 'email': 'aditya.sharma@example.com', 'role': 'Manager'},
        {'id': 4, 'name': 'Sai Gupta', 'email': 'sai.gupta@example.com', 'role': 'Developer'},
        {'id': 5, 'name': 'Arjun Singh', 'email': 'arjun.singh@example.com', 'role': 'Analyst'},
        {'id': 6, 'name': 'Ananya Reddy', 'email': 'ananya.reddy@example.com', 'role': 'Designer'},
        {'id': 7, 'name': 'Diya Verma', 'email': 'diya.verma@example.com', 'role': 'Developer'},
        {'id': 8, 'name': 'Ishaan Kumar', 'email': 'ishaan.kumar@example.com', 'role': 'Manager'},
        {'id': 9, 'name': 'Myra Joshi', 'email': 'myra.joshi@example.com', 'role': 'Tester'},
        {'id': 10, 'name': 'Rohan Mehta', 'email': 'rohan.mehta@example.com', 'role': 'Developer'},
    ]
    return render(request, 'core/user_list.html', {'users': users})
