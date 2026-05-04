export function MetricsTable() {
  return (
    <div className="card">
      <h3 className="font-semibold mb-3">Метрики</h3>
      <table className="w-full text-sm">
        <thead><tr><th className="text-left">Метрика</th><th>Факт</th><th>Цель</th><th>Отклонение</th></tr></thead>
        <tbody>
          <tr><td>Food Cost %</td><td className="text-center">38</td><td className="text-center">32</td><td className="text-risk text-center">+6</td></tr>
          <tr><td>Labor Cost %</td><td className="text-center">29</td><td className="text-center">30</td><td className="text-ok text-center">-1</td></tr>
        </tbody>
      </table>
    </div>
  );
}
