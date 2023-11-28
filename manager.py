import netlify.functions as nf
import os
from faunadb import query as q
from faunadb.client import Client

def student_attendance(event, context):
    student_name = event['body']['student_name']
    class_name = event['body']['class_name']

    # Connect to the database using the Netlify Functions environment variable
    faunadb_secret = os.environ['FAUNADB_SECRET']
    client = Client(secret=faunadb_secret)

    # Create a new attendance record in the database
    attendance_record = q.Create(q.Ref('classes', class_name), {
        data: {
            student_name: student_name,
            date: q.ToDate(q.Now()),
            status: 'present'
        }
    })

    # Execute the query and handle the response
    try:
        result = client.query(attendance_record)
        return nf.jsonResponse({'message': 'Student attendance recorded successfully.'})
    except Exception as e:
        print(e)
        return nf.jsonResponse({'message': 'Failed to record student attendance.'}, status=500)
