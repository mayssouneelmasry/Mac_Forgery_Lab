from flask import Flask, render_template, request
import hashpumpy
import hmac
import hashlib

app = Flask(__name__)

SECRET_KEY = b'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    mac = ''
    mode = request.args.get('mode', 'insecure')
    step = request.form.get('step') if request.method == 'POST' else None

    if request.method == 'POST':
        original = request.form['original']
        append = request.form.get('append', '')
        if append is None:
            append = ''

        if step == 'generate_mac':
            if mode == 'insecure':
                mac = hashlib.md5(SECRET_KEY + original.encode()).hexdigest()
            else:
                mac = hmac.new(SECRET_KEY, original.encode(), hashlib.md5).hexdigest()
            result = {
                'step': 'generate_mac',
                'original': original,
                'mac': mac,
                'mode': mode,
                'full_output': f"=== Server Simulation ===\nOriginal message: {original}\nMAC: {mac}\nMAC generated successfully."
            }
            return render_template('index.html', result=result, mode=mode)

        elif step == 'forge_mac':
            mac = request.form.get('mac')
            if not mac:
                result = {
                    'step': 'forge_mac',
                    'error': 'MAC is required for performing the attack or verification.'
                }
                return render_template('index.html', result=result, mode=mode)

            if mode == 'insecure':
                full_output = [
                    f"=== Client Simulation ===",
                    f"Original: {original}",
                    f"Intercepted MAC: {mac}",
                    f"Data to append: {append}\n"
                ]
                success = False
                for key_len in range(8, 22):
                    try:
                        # Use dummy data if append is empty for demo purposes
                        demo_append = append if append else chr(104 + (key_len % 5))  # 'h', 'i', etc.
                        new_mac, new_message = hashpumpy.hashpump(mac, original, demo_append, key_len)
                        expected_mac = hashlib.md5(SECRET_KEY + new_message).hexdigest()

                        full_output.append(f"Trying key length guess: {key_len}")
                        full_output.append(f"  Forged message: {new_message}")
                        full_output.append(f"  Forged MAC: {new_mac}")

                        if new_mac == expected_mac:
                            full_output.append("✅ SUCCESSFUL FORGERY (Correct Key Length)")
                            result = {
                                'step': 'forge_mac',
                                'mode': 'Insecure (Vulnerable to Forgery)',
                                'key_length': key_len,
                                'forged_mac': new_mac,
                                'forged_message': new_message,
                                'full_output': "\n".join(full_output)
                            }
                            success = True
                            break
                        else:
                            full_output.append("❌ Verification failed.\n")
                    except Exception as e:
                        full_output.append(f"Error at key length {key_len}: {str(e)}\n")

                if not success:
                    result = {
                        'step': 'forge_mac',
                        'mode': 'Insecure (Forgery Failed)',
                        'full_output': "\n".join(full_output) + "\n❌ Forgery unsuccessful for all key length guesses."
                    }

            else:
                full_message = (original + append).encode()
                is_valid = (mac == hmac.new(SECRET_KEY, full_message, hashlib.md5).hexdigest())
                verification_text = "MAC verified successfully. Message is authentic." if is_valid else "MAC verification failed (as expected, secure implementation)."
                result = {
                    'step': 'forge_mac',
                    'mode': 'Secure (HMAC)',
                    'is_valid': is_valid,
                    'combined_message': full_message.decode(errors='ignore'),
                    'full_output': f"=== Secure Server Simulation ===\nOriginal message: {original}\nAppended: {append}\nCombined Message: {full_message.decode(errors='ignore')}\nUser-supplied MAC: {mac}\n\n--- Verifying message ---\n{verification_text}"
                }

    return render_template('index.html', result=result, mode=mode)

if __name__ == '__main__':
    app.run(debug=True)
