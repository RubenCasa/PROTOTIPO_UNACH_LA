// AUTO-GENERATED ML MODEL
// Exported from Python scikit-learn using m2cgen

/**
 * Predice el nivel de riesgo en base a 3 features: [asistencia, nota_final, total_eventos]
 * Retorna: 0 (Alto Riesgo), 1 (Riesgo Medio), 2 (Riesgo Bajo)
 */
export function predictRisk(input) {
function score(input) {
    var var0;
    if (input[1] <= 5.950000047683716) {
        var0 = [1.0, 0.0, 0.0];
    } else {
        if (input[1] <= 7.450000047683716) {
            var0 = [0.0, 1.0, 0.0];
        } else {
            if (input[0] <= 79.5) {
                var0 = [0.0, 1.0, 0.0];
            } else {
                var0 = [0.0, 0.0, 1.0];
            }
        }
    }
    return var0;
}

  // m2cgen returns an array with scores for each class [score0, score1, score2]
  const scores = score(input);
  // Devuelve el indice del maximo score
  return scores.indexOf(Math.max(...scores));
}
