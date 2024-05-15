from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import openai

# Set your OpenAI API key here
openai.api_key = 'api key'

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if 'question' in data:
            question = data['question']
            answer = generate_answer(question)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'answer': answer}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()
            response = {'error': 'No question provided.'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

def generate_answer(question):
    response = openai.Completion.create(
        engine="davinci",
        prompt=question,
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
