    # Plot
    fig, ax = plt.subplots(figsize=(16, 6))

    for i, status in enumerate(statuses):
        scores = []
        responses = []

        for vert in verticals:
            row = region_df[(region_df['Vertical'] == vert) & (region_df['Status'] == status)]
            if not row.empty:
                scores.append(row['NPS_Score'].values[0])
                responses.append(int(row['Responses'].values[0]))
            else:
                scores.append(0)
                responses.append(0)

        bar_x = x + (i - 1) * width
        bars = ax.bar(bar_x, scores, width=width, label=status, color=color_map.get(status, 'gray'))

        # ✅ Always show labels, even if zero or negative
        for j, bar in enumerate(bars):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (1 if scores[j] >= 0 else -4),
                    f"{scores[j]:.1f}%\n{responses[j]}R", ha='center', fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(verticals, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel("NPS Score (%)")

    # ✅ Adjust y-axis to show negatives
    min_score = min(region_df['NPS_Score'].min(), 0)
    max_score = max(region_df['NPS_Score'].max(), 100)
    ax.set_ylim(min_score - 10, max_score + 10)

    ax.set_title(f"📊 Cumulative NPS by Vertical – {selected_region}")
    ax.legend(title="Batch Status", bbox_to_anchor=(1.02, 1), loc='upper left')

    st.pyplot(fig)
