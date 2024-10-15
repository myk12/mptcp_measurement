import os

input_dir="./domain_ip/"

class d2s_processor:
    def __init__(self):
        self.domain_ip_dict = {}
    
    def load_results_from_files(self, input_dir):
        for file in os.listdir(input_dir):
            print("Processing file: "+file)
            if file.endswith(".dat"):
                with open(input_dir+file, "r") as f:
                    for line in f:
                        #skip the first line
                        if line.startswith("Domain"):
                            continue
                        elem_list = line.split(',')
                        domain = elem_list[0].strip()
                        ip_list = []
                        for i in range(1, len(elem_list)):
                            ip = elem_list[i].strip()
                            ip_list.append(ip)
                        self.domain_ip_dict[domain] = ip_list
                        print("Domain: "+domain+" IP: "+str(ip_list))

    def export_pure_ip_list(self, output_file):
        with open(output_file, "w") as f:
            for domain in self.domain_ip_dict:
                ip_list = self.domain_ip_dict[domain]
                for ip in ip_list:
                    f.write(ip+"\n")
    
    def export_domain_ip_list(self, output_file):
        with open(output_file, "w") as f:
            for domain in self.domain_ip_dict:
                ip_list = self.domain_ip_dict[domain]
                f.write(domain)
                for ip in ip_list:
                    f.write(","+ip)
                f.write("\n")

if __name__ == "__main__":
    processor = d2s_processor()
    processor.load_results_from_files(input_dir)
    processor.export_pure_ip_list("ip_list.dat")
