allowed_ips = [
    '192.168.1.1',
    '192.168.1.2',
    '10.0.0.1'
]

def filter_ips(input_file_path, output_file_path, allowed_ips):
    ip_counts = {}

    try:
        with open(input_file_path, 'r') as file:
            for line in file:
                ip_address = line.split()[0]

                if ip_address in allowed_ips:
                    if ip_address in ip_counts:
                        ip_counts[ip_address] += 1
                    else:
                        ip_counts[ip_address] = 1

    except FileNotFoundError:
        print(f"Input file {input_file_path} not found")
        return

    try:
        with open(output_file_path, 'w') as file:
            for ip_address in ip_counts:
                file.write(f"{ip_address} - {ip_counts[ip_address]}\n")

    except IOError:
        print(f"Error writing to output file {output_file_path}")

    print(ip_counts)

filter_ips('access.log', 'result.txt', allowed_ips)
