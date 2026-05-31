import re

with open(r'd:\Download\Cost\Html\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start and end of the renderBookmarks function
start_marker = '        function renderBookmarks() {\n            const list = document.getElementById(\'bookmarks-modal-list\');'
end_marker = '        // Bookmark Index Event Handlers'

start_idx = content.find('        function renderBookmarks()')
end_idx = content.find('        // Bookmark Index Event Handlers')

if start_idx == -1:
    print("ERROR: Could not find renderBookmarks start")
    exit(1)
if end_idx == -1:
    print("ERROR: Could not find end marker")
    exit(1)

print(f"Found renderBookmarks at line positions {start_idx} to {end_idx}")

new_function = '''        function renderBookmarks() {
            const list = document.getElementById('bookmarks-modal-list');
            const badge = document.getElementById('bm-badge-count');
            const subtitle = document.getElementById('bm-modal-subtitle');
            const emptyState = document.getElementById('bookmarks-modal-empty');
            const bookmarks = getBookmarks();

            if (badge) {
                if (bookmarks.length > 0) {
                    badge.textContent = bookmarks.length;
                    badge.classList.remove('hidden');
                } else {
                    badge.classList.add('hidden');
                }
            }

            if (subtitle) {
                subtitle.textContent = bookmarks.length + ' \u0639\u0646\u0627\u0635\u0631 \u0645\u062d\u0641\u0648\u0638\u0629 \u0644\u0644\u0645\u0631\u0627\u062c\u0639\u0629';
            }

            if (!list) return;

            if (bookmarks.length === 0) {
                list.innerHTML = '';
                if (emptyState) emptyState.classList.remove('hidden');
                return;
            }

            if (emptyState) emptyState.classList.add('hidden');
            list.innerHTML = '';

            bookmarks.forEach((bm, idx) => {
                const card = document.createElement('div');
                const isLec = (bm.type === 'lecture');
                const borderHex = isLec ? '#a855f7' : '#f59e0b';
                const hoverShadow = isLec ? '0 8px 24px rgba(168,85,247,0.15)' : '0 8px 24px rgba(245,158,11,0.15)';
                const headerBg = isLec ? '#faf5ff' : '#fffbeb';
                const mainIcon = isLec ? 'fa-solid fa-graduation-cap' : 'fa-solid fa-bookmark';
                const mainIconColor = isLec ? '#7e22ce' : '#b45309';
                const mainIconBg = isLec ? '#f3e8ff' : '#fef9c3';
                const mainIconBorder = isLec ? '#e9d5ff' : '#fcd34d';

                card.style.cssText = `background:white; border-radius:1rem; border:2px solid ${borderHex}; overflow:hidden; box-shadow:0 2px 12px rgba(0,0,0,0.06); transition:box-shadow 0.2s;`;
                card.onmouseover = () => card.style.boxShadow = hoverShadow;
                card.onmouseout = () => card.style.boxShadow = '0 2px 12px rgba(0,0,0,0.06)';

                if (isLec) {
                    const cleanTitle = (bm.lectureTitle || '').replace('\u0627\u0644\u0645\u062d\u0627\u0636\u0631\u0629 ', '\u0645\u062d\u0627\u0636\u0631\u0629 ');
                    const cardTitle = (bm.cardTitle || '').replace(/<[^>]+>/g, '');

                    card.innerHTML = `
                        <div onclick="toggleBookmarkCard(${idx})" style="display:flex; align-items:flex-start; justify-content:space-between; gap:0.6rem; padding:0.85rem 1rem; cursor:pointer; background:${headerBg};">
                            <div style="display:flex; align-items:flex-start; gap:0.6rem; min-width:0; flex:1;">
                                <div style="width:2rem; height:2rem; min-width:2rem; background:${mainIconBg}; border:1.5px solid ${mainIconBorder}; border-radius:0.5rem; display:flex; align-items:center; justify-content:center; color:${mainIconColor}; font-size:0.85rem; margin-top:0.1rem;">
                                    <i class="${mainIcon}"></i>
                                </div>
                                <div style="flex:1; min-width:0;">
                                    <div style="display:flex; align-items:center; gap:0.35rem; margin-bottom:0.3rem; flex-wrap:wrap;">
                                        <span style="font-size:0.62rem; font-weight:900; background:#f3e8ff; color:#6b21a8; padding:0.1rem 0.4rem; border-radius:0.3rem; white-space:nowrap;">\u0634\u0631\u062d \u0644\u0644\u0645\u0631\u0627\u062c\u0639\u0629</span>
                                        <span style="font-size:0.62rem; font-weight:800; background:#f0fdf4; color:#166534; padding:0.1rem 0.4rem; border-radius:0.3rem; border:1px solid #86efac; white-space:nowrap;">${cleanTitle}</span>
                                        <span style="font-size:0.6rem; color:#94a3b8; font-weight:600;">${bm.savedAt || ''}</span>
                                    </div>
                                    <div style="font-size:0.85rem; font-weight:800; color:#1e293b; direction:rtl; text-align:right; word-break:break-word; line-height:1.45;">${cardTitle || ''}</div>
                                </div>
                            </div>
                            <div style="display:flex; align-items:center; gap:0.3rem; flex-shrink:0; padding-top:0.05rem;">
                                <button onclick="event.stopPropagation(); navigateToLectureCardByIdx(${idx})" title="\u0639\u0631\u0636 \u0641\u064a \u0627\u0644\u0645\u062d\u0627\u0636\u0631\u0629" style="width:1.7rem; height:1.7rem; border-radius:0.4rem; border:1.5px solid #c084fc; background:#faf5ff; color:#7e22ce; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:0.72rem;" onmouseover="this.style.background=\'#f3e8ff\'" onmouseout="this.style.background=\'#faf5ff\'">
                                    <i class="fa-solid fa-eye"></i>
                                </button>
                                <button onclick="event.stopPropagation(); openAIChatForBookmarkByIdx(${idx})" title="\u0627\u0633\u0623\u0644 AI" style="width:1.7rem; height:1.7rem; border-radius:0.4rem; border:1.5px solid #10b981; background:#ecfdf5; color:#047857; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:0.72rem;" onmouseover="this.style.background=\'#d1fae5\'" onmouseout="this.style.background=\'#ecfdf5\'">
                                    <i class="fa-solid fa-robot"></i>
                                </button>
                                <button onclick="event.stopPropagation(); deleteBookmarkByIdx(${idx})" title="\u062d\u0630\u0641" style="width:1.7rem; height:1.7rem; border-radius:0.4rem; border:1.5px solid #fca5a5; background:#fff5f5; color:#dc2626; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:0.72rem;" onmouseover="this.style.background=\'#fee2e2\'" onmouseout="this.style.background=\'#fff5f5\'">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                                <i id="bm-chevron-${idx}" class="fa-solid fa-chevron-down" style="color:#94a3b8; font-size:0.78rem; transition:transform 0.3s;"></i>
                            </div>
                        </div>
                        <div id="bm-body-${idx}" style="display:none; padding:1rem; border-top:1.5px solid #f3e8ff; background:#fff;">
                            ${bm.enText ? `
                            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:0.6rem; padding:0.85rem; font-size:0.82rem; font-weight:600; color:#334155; line-height:1.75; overflow-x:auto; direction:ltr; text-align:left; word-break:break-word;">
                                ${bm.enText}
                            </div>` : ''}
                            ${bm.arText ? `
                            <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:0.6rem; padding:0.85rem; font-size:0.83rem; font-weight:700; color:#78350f; line-height:1.8; direction:rtl; text-align:right; margin-top:0.65rem; word-break:break-word;">
                                ${bm.arText}
                            </div>` : ''}
                        </div>
                    `;
                } else {
                    const examBg = bm.examId === 'cost_1_s' ? '#e0e7ff' : '#ede9fe';
                    const examColor = bm.examId === 'cost_1_s' ? '#3730a3' : '#5b21b6';
                    const qTextClean = (bm.qText || '').replace(/<[^>]+>/g,'');

                    card.innerHTML = `
                        <div onclick="toggleBookmarkCard(${idx})" style="display:flex; align-items:flex-start; justify-content:space-between; gap:0.6rem; padding:0.85rem 1rem; cursor:pointer; background:${headerBg};">
                            <div style="display:flex; align-items:flex-start; gap:0.6rem; min-width:0; flex:1;">
                                <div style="width:2rem; height:2rem; min-width:2rem; background:${mainIconBg}; border:1.5px solid ${mainIconBorder}; border-radius:0.5rem; display:flex; align-items:center; justify-content:center; color:${mainIconColor}; font-size:0.85rem; margin-top:0.1rem;">
                                    <i class="${mainIcon}"></i>
                                </div>
                                <div style="flex:1; min-width:0;">
                                    <div style="display:flex; align-items:center; gap:0.35rem; margin-bottom:0.3rem; flex-wrap:wrap;">
                                        <span style="font-size:0.62rem; font-weight:900; background:${examBg}; color:${examColor}; padding:0.1rem 0.4rem; border-radius:0.3rem; white-space:nowrap;">${bm.examTitle || bm.examId}</span>
                                        <span style="font-size:0.62rem; font-weight:800; background:#f0fdf4; color:#166534; padding:0.1rem 0.4rem; border-radius:0.3rem; border:1px solid #86efac; white-space:nowrap;">\u0633\u0624\u0627\u0644 ${(bm.qIndex || 0) + 1}</span>
                                        <span style="font-size:0.6rem; color:#94a3b8; font-weight:600;">${bm.savedAt || ''}</span>
                                    </div>
                                    <div style="font-size:0.83rem; font-weight:700; color:#1e293b; direction:ltr; text-align:left; word-break:break-word; line-height:1.4;">${qTextClean.slice(0,150)}${qTextClean.length > 150 ? '...' : ''}</div>
                                    ${bm.note ? `<div style="font-size:0.72rem; color:#92400e; font-weight:700; margin-top:0.2rem; direction:rtl; text-align:right; word-break:break-word;"><i class="fa-solid fa-pen" style="font-size:0.6rem;"></i> ${bm.note}</div>` : ''}
                                </div>
                            </div>
                            <div style="display:flex; align-items:center; gap:0.3rem; flex-shrink:0; padding-top:0.05rem;">
                                <button onclick="event.stopPropagation(); openAIChatForBookmarkByIdx(${idx})" title="\u0627\u0633\u0623\u0644 AI" style="width:1.7rem; height:1.7rem; border-radius:0.4rem; border:1.5px solid #10b981; background:#ecfdf5; color:#047857; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:0.72rem;" onmouseover="this.style.background=\'#d1fae5\'" onmouseout="this.style.background=\'#ecfdf5\'">
                                    <i class="fa-solid fa-robot"></i>
                                </button>
                                <button onclick="event.stopPropagation(); deleteBookmarkByIdx(${idx})" title="\u062d\u0630\u0641" style="width:1.7rem; height:1.7rem; border-radius:0.4rem; border:1.5px solid #fca5a5; background:#fff5f5; color:#dc2626; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:0.72rem;" onmouseover="this.style.background=\'#fee2e2\'" onmouseout="this.style.background=\'#fff5f5\'">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                                <i id="bm-chevron-${idx}" class="fa-solid fa-chevron-down" style="color:#94a3b8; font-size:0.78rem; transition:transform 0.3s;"></i>
                            </div>
                        </div>
                        <div id="bm-body-${idx}" style="display:none; padding:1rem; border-top:1.5px solid #fef3c7; background:#fff;">
                            <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:0.6rem; padding:0.6rem 0.85rem; margin-bottom:0.65rem; font-size:0.82rem; font-weight:700; color:#166534; direction:ltr; text-align:left; word-break:break-word;">
                                <strong style="color:#166534;">\u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0627\u0644\u0635\u062d\u064a\u062d\u0629:</strong> ${bm.correctText || bm.correct || ''}
                            </div>
                            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:0.6rem; padding:0.85rem; font-size:0.82rem; font-weight:600; color:#475569; line-height:1.75; overflow-x:auto; max-height:280px; overflow-y:auto; direction:ltr; text-align:left; word-break:break-word;">
                                <div style="font-size:0.76rem; font-weight:800; color:#4f46e5; display:flex; align-items:center; gap:0.35rem; margin-bottom:0.5rem;">
                                    <i class="fa-solid fa-chalkboard-user"></i> \u0627\u0644\u0634\u0631\u062d \u0627\u0644\u062a\u0641\u0635\u064a\u0644\u064a:
                                </div>
                                ${bm.explanation || ''}
                            </div>
                            ${bm.note ? `
                            <div style="background:#fef9c3; border:1.5px solid #fcd34d; border-radius:0.6rem; padding:0.6rem 0.85rem; margin-top:0.65rem; font-size:0.83rem; font-weight:700; color:#92400e; direction:rtl; text-align:right; word-break:break-word;">
                                <i class="fa-solid fa-pen" style="margin-left:0.3rem;"></i> \u0645\u0644\u0627\u062d\u0638\u062a\u064a: ${bm.note}
                            </div>` : ''}
                        </div>
                    `;
                }
                list.appendChild(card);
            });

            if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
                MathJax.typesetPromise([list]);
            }
        }

        '''

new_content = content[:start_idx] + new_function + content[end_idx:]

with open(r'd:\Download\Cost\Html\index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done! renderBookmarks function replaced successfully.")
print(f"New file size: {len(new_content)} bytes")
