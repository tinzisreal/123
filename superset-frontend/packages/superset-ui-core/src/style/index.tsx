/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import emotionStyled from '@emotion/styled';
import { useTheme as useThemeBasic } from '@emotion/react';
import createCache from '@emotion/cache';

export {
  css,
  keyframes,
  jsx,
  ThemeProvider,
  CacheProvider as EmotionCacheProvider,
  withTheme,
} from '@emotion/react';
export { default as createEmotionCache } from '@emotion/cache';

declare module '@emotion/react' {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  export interface Theme extends SupersetTheme {}
}

export function useTheme() {
  const theme = useThemeBasic();
  // in the case there is no theme, useTheme returns an empty object
  if (Object.keys(theme).length === 0 && theme.constructor === Object) {
    throw new Error(
      'useTheme() could not find a ThemeContext. The <ThemeProvider/> component is likely missing from the app.',
    );
  }
  console.log("🎨 useTheme() hook called:", theme);  // 👉 log test
  return theme;
}

export const emotionCache = createCache({
  key: 'superset',
});

export const styled = emotionStyled;

const defaultTheme = {
  borderRadius: 4,
  colors: {
    text: {
      label: '#879399',
      help: '#737373',
    },
    primary: {
      base: '#8e2e2eff',   // 🔵 xanh dương chủ đạo
      dark1: '#1565C0',
      dark2: '#0D47A1',
      light1: '#42A5F5',
      light2: '#90CAF9',
      light3: '#BBDEFB',
      light4: '#E3F2FD',
      light5: '#F5F9FF',
    },
    secondary: {
      base: '#FFC107',   // 🟡 vàng phụ
      dark1: '#FFA000',
      dark2: '#FF8F00',
      dark3: '#FF6F00',
      light1: '#FFD54F',
      light2: '#FFE082',
      light3: '#FFECB3',
      light4: '#FFF8E1',
      light5: '#FFFFF9',
    },
    grayscale: {
      base: '#666666',
      dark1: '#323232',
      dark2: '#000000',
      light1: '#B2B2B2',
      light2: '#E0E0E0',
      light3: '#F0F0F0',
      light4: '#F7F7F7',
      light5: '#FFFFFF',
    },
    error: {
      base: '#E04355',
      dark1: '#A7323F',
      dark2: '#6F212A',
      light1: '#EFA1AA',
      light2: '#FAEDEE',
    },
    warning: {
      base: '#FF9800',
      dark1: '#F57C00',
      dark2: '#E65100',
      light1: '#FFB74D',
      light2: '#FFE0B2',
    },
    alert: {
      base: '#FCC700',
      dark1: '#BC9501',
      dark2: '#7D6300',
      light1: '#FDE380',
      light2: '#FEF9E6',
    },
    success: {
      base: '#4CAF50',
      dark1: '#388E3C',
      dark2: '#2E7D32',
      light1: '#81C784',
      light2: '#C8E6C9',
    },
    info: {
      base: '#2196F3',
      dark1: '#1976D2',
      dark2: '#0D47A1',
      light1: '#64B5F6',
      light2: '#BBDEFB',
    },
  },
  opacity: {
    light: '10%',
    mediumLight: '35%',
    mediumHeavy: '60%',
    heavy: '80%',
  },
  typography: {
    families: {
      sansSerif: `'Inter', Helvetica, Arial`,
      serif: `Georgia, 'Times New Roman', Times, serif`,
      monospace: `'Fira Code', 'Courier New', monospace`,
    },
    weights: {
      light: 200,
      normal: 400,
      medium: 500,
      bold: 600,
    },
    sizes: {
      xxs: 9,
      xs: 10,
      s: 12,
      m: 14,
      l: 16,
      xl: 21,
      xxl: 28,
    },
  },
  zIndex: {
    aboveDashboardCharts: 10,
    dropdown: 11,
    max: 3000,
  },
  transitionTiming: 0.3,
  gridUnit: 4,
  brandIconMaxWidth: 37,
};

console.log("🎨 Superset defaultTheme loaded:", defaultTheme); // 👉 log test

export type SupersetTheme = typeof defaultTheme;

export interface SupersetThemeProps {
  theme: SupersetTheme;
}

export const supersetTheme = defaultTheme;
