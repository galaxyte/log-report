There is an Apache-style access log at /app/access.log. Parse it and write a
summary report to /app/report.json as a single JSON object with exactly these
keys:

- "total_requests": integer, the number of log lines (requests) in the file.
- "unique_ips": integer, the number of distinct client IP addresses.
- "top_path": string, the request path (e.g. "/index.html") that appears most
  often across all requests. Break ties by picking the path that appears first
  in the log.

Success criteria:
1. /app/report.json exists and contains valid JSON.
2. The JSON object has exactly the keys "total_requests", "unique_ips", and
   "top_path"; it has no additional keys.
3. "total_requests" equals the true number of non-empty request lines in
   /app/access.log.
4. "unique_ips" equals the true number of distinct client IPs in the log.
5. "top_path" equals the actual most-requested path in the log, using the
   first path encountered in the log to break a tie.
