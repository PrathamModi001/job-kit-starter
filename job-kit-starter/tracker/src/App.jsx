import { useMemo, useState } from 'react'
import DATA from './data.json'
import META from './meta.json'

const STATUS_CHIPS = [
  ['Applied', 'Applied'],
  ['Drafting', 'Drafting'],
  ['Lead', 'Leads'],
  ['Skipped', 'Skipped'],
  ['Closed', 'Closed'],
  ['*', 'Everything'],
]

const STAT_DEFS = [
  ['Applied', 'Applied', true],
  ['Lead', 'Leads', false],
  ['Drafting', 'Drafting', false],
  ['Skipped', 'Skipped', false],
  ['Closed', 'Closed', false],
]

export default function App() {
  const [filter, setFilter] = useState('Applied')
  const [q, setQ] = useState('')

  const counts = useMemo(() => {
    const c = {}
    for (const d of DATA) c[d.status] = (c[d.status] || 0) + 1
    return c
  }, [])

  const platforms = useMemo(() => {
    const p = {}
    for (const d of DATA) if (d.status === 'Applied') p[d.via] = (p[d.via] || 0) + 1
    return Object.entries(p).sort((a, b) => b[1] - a[1])
  }, [])

  const rows = useMemo(() => {
    const ql = q.trim().toLowerCase()
    return DATA.filter(d =>
      (filter === '*' || d.status === filter) &&
      (!ql || `${d.co} ${d.role} ${d.via} ${d.found} ${d.loc} ${d.resume || ''}`.toLowerCase().includes(ql)))
  }, [filter, q])

  return (
    <div className="wrap">
      <header>
        <h1>Application Tracker</h1>
        <span className="sub">updated {META.updated} &middot; sourced from applications.csv</span>
      </header>

      <div className="stats">
        <div className="stat"><b>{DATA.length}</b><span>Total tracked</span></div>
        {STAT_DEFS.map(([key, label, hl]) => (
          <div className={hl ? 'stat hl' : 'stat'} key={key}>
            <b>{counts[key] || 0}</b><span>{label}</span>
          </div>
        ))}
      </div>

      <p className="plat">
        Applications by platform:{' '}
        {platforms.map(([k, v], i) => (
          <span key={k}>{i > 0 && ' · '}<b>{v}</b>&nbsp;{k}</span>
        ))}
      </p>

      <div className="controls">
        {STATUS_CHIPS.map(([key, label]) => (
          <button key={key}
            className={filter === key ? 'chipbtn on' : 'chipbtn'}
            onClick={() => setFilter(key)}>{label}</button>
        ))}
        <input id="q" type="search" value={q} aria-label="Search"
          placeholder="Search company, role, platform…"
          onChange={e => setQ(e.target.value)} />
      </div>

      <div className="tablebox">
        <table>
          <thead>
            <tr>
              <th>Company &amp; role</th><th>Applied on</th><th>Found via</th>
              <th>Resume</th><th>Comp</th><th>Date</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((d, i) => (
              <tr key={`${d.co}-${d.role}-${i}`}>
                <td className="co">
                  {d.url
                    ? <a href={d.url} target="_blank" rel="noopener noreferrer">{d.co}</a>
                    : <span style={{ fontWeight: 650 }}>{d.co}</span>}
                  <span className="role">{d.role}</span>
                </td>
                <td><span className="tag">{d.via}</span></td>
                <td><span className="tag">{d.found}</span></td>
                <td className="resume" title={d.resume}>{d.resume
                  ? <span className="tag resume-tag">{d.resume.replace(/^.*[\\/]/, '')}</span>
                  : <span className="muted">—</span>}</td>
                <td className="comp" title={d.comp}>{d.comp || '—'}</td>
                <td className="num">{d.date}</td>
                <td><span className={`pill s-${d.status}`}>{d.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length === 0 && <div className="empty">Nothing matches.</div>}
      </div>

      <footer>
        Company name links to the original posting. &ldquo;Applied on&rdquo; = platform the
        application was submitted through; &ldquo;Found via&rdquo; = where the listing was discovered;
        &ldquo;Resume&rdquo; = the exact tailored resume file sent for that application.
      </footer>
    </div>
  )
}
