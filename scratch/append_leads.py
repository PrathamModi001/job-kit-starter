import subprocess, json

p = {
    'Company': 'Lab0',
    'Role': 'Forward Deployed Engineer (FDE)',
    'Location': 'Bengaluru, Karnataka, IN',
    'Channel': 'WaaS (Work at a Startup)',
    'Comp': '$30K - $55K (~25-46 LPA)',
    'Status': 'Applied',
    'Resume': 'output/Lab0 - Forward Deployed Engineer/Pratham_Modi_Resume.pdf',
    'Job URL': 'https://www.workatastartup.com/jobs/111521',
    'Next step': 'Applied via WaaS with tailored AI & Backend Systems resume and custom pitch note to Lakshya; confirmed with "Applied" status.',
    'Personal Info Filled': "name=Pratham Modi; email=prathammodi001@gmail.com; intro_pitch=Hi Lakshya, I'm Pratham Modi, a backend and AI systems engineer based in Bengaluru...; achievement=At C3iHub, I architected the core LMS backend and national hackathon platform handling 10,000+ concurrent connections and 75K+ daily Kafka events with 99.9% uptime, while reducing cloud storage costs 60% and cutting p99 latency from 450ms to 135ms."
}
subprocess.run(['python', r'E:\Extra\job-kit-starter\scratch\csv_updater.py', json.dumps(p)], check=True)
