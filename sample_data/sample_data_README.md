# Sample Data Files

- `resume_strong.pdf` + `jd_strong.txt`: Special Needs Program Coordinator resume and matching job description (tests high match score).
- `resume_weak.pdf`: Commercial Real Estate Broker resume tested against `jd_strong.txt` (tests low match score on unrelated field).
- `resume_unusual_headings.pdf`: Marketing resume using non-standard headings like "Who I Am" and "What I Do" (tests section heading validation warning).
- `resume_scanned.pdf`: Image-only PDF created from a rendered page with no selectable text layer (tests scanned PDF `ValueError` handling).
- `not_a_resume.pdf`: Operating Systems homework assignment document (tests non-resume document yellow warning).
- `resume_cpp_dotnet.pdf` + `jd_cpp.txt`: Software Engineer resume and JD containing `C++`, `C#`, and `.NET` (tests special character preservation in `clean_text` and matcher).
